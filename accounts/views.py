from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ProfileForm, ExperienceForm, EducationForm
from .models import Profile, Skill, Education, Experience
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DeleteView, UpdateView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib.messages.views import SuccessMessageMixin

def index(request):
  return render(request, 'index.html')

@login_required
def profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = ProfileForm(data=request.POST, files=request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.user.first_name = request.POST.get('first_name', '')  
            profile.user.last_name = request.POST.get('last_name', '')  
            profile.user.save()  
            profile.save()  
            skill_names = form.cleaned_data.get('skills', [])
            skills = []
            for name in skill_names:
                skill = get_object_or_404(Skill, name=name)
                skills.append(skill)
            profile.skills.set(skills)
            return redirect('dashboard')
    else:
        initial_skills = [skill.name for skill in profile.skills.all()] if profile else []
        form = ProfileForm(instance=profile, initial={'skills': initial_skills})

    context = {'profile': profile, 'form': form}
    if form.errors:
        context['error_message'] = 'Form is invalid. Please correct the errors below.'

    return render(request, 'account/profile.html', context)




def profile_detail(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    context = {'profile': profile}
    return render(request, 'account/profile_detail.html', context)

@login_required
def dashboard(request):
  return render(request, 'account/dashboard.html')

def profiles(request):
    """
    Renders a list of profiles.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: A rendered HTML response containing the list of profiles.
    """

    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(request, 'account/profiles.html', context)

class ExperienceCreateView(LoginRequiredMixin, CreateView):
    model = Experience
    form_class = ExperienceForm
    template_name = 'account/add_experience.html'
    success_message = 'Experience created successfully!'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = self.request.user
        kwargs['initial'] = {'profile': user.profile}
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['experiences'] = Experience.objects.filter(profile=self.request.user.profile)
        return context

    def get_success_url(self):
        return reverse_lazy('add_experience')
    
    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        return super().form_valid(form)
    
class ExperienceUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Experience
    form_class = ExperienceForm
    template_name = 'account/edit_experience.html'  
    success_message = 'Experience updated successfully!'

    def get_success_url(self):
        return reverse_lazy('add_experience')  

    def form_valid(self, form):
        print("Form is valid")
        response = super().form_valid(form)
        if self.request.is_ajax():
            return JsonResponse({'success': True})  
        else:
            return response  

    def form_invalid(self, form):
        print("Form is invalid")
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)  
        else:
            return response  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        experience = self.get_object()  # Retrieve the experience object
        print("Experience:", experience)
        context['experience'] = experience
        return context


@method_decorator(login_required, name='dispatch')
class ExperienceDeleteView(DeleteView):
    model = Experience
    success_url = reverse_lazy('add_experience')

@login_required
def add_education(request):
    """
    Renders a form for users to create or edit education data.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: A rendered HTML response containing the form.
    """

    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            # Process valid form data here (save to database, etc.)
            form.save()  # Assuming you want to save the form data
            return render(request, 'education_success.html', {'message': 'Education saved successfully!'})
    else:
        form = EducationForm()

    context = {'form': form}
    return render(request, 'account/add_education.html', context)
