from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ProfileForm, ExperienceForm, EducationForm
from .models import Profile, Skill, Education, Experience
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model

def index(request):
  User = get_user_model()
  if request.user.is_authenticated:
    return redirect('dashboard') 
  else:
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
    
    if request.headers.get('accept') == 'application/json':
        # Serialize profile data into a dictionary
        profile_data = {
            'id': profile.pk,
            'user_id': profile.user.id,
            'username': profile.user.username,
            'email': profile.user.email,
            'company': profile.company,
            'website': profile.website,
            'location': profile.location,
            'bio': profile.bio,
            'githubusername': profile.githubusername,
            'date': profile.date.strftime('%Y-%m-%d %H:%M:%S'),
            'image_url': profile.image.url if profile.image else '',
            'occupation': profile.occupation,
            'skills': list(profile.skills.values_list('name', flat=True))
        }
        
        # Return JSON response
        return JsonResponse(profile_data)
    else:
        # Render template for HTML response
        context = {'profile': profile}
        return render(request, 'account/profile_detail.html', context)

@login_required
def dashboard(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'account/dashboard.html', context)

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

#experiance related views
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
        
        # Add the newly created experience to the context
        if self.object:
            experience = self.object.pk
            print("Newly created experience PK:", experience)
            context['experience'] = experience
        
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
        return reverse_lazy('add_experience')  # Consider redirecting to a more relevant page

    def form_valid(self, form):
        form.save()  # Save the updated experience
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        experience = self.get_object()  # Retrieve the experience object
        context['experience'] = experience
        return context

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.kwargs['pk'])

class ExperienceDetailView(LoginRequiredMixin, DetailView):
    model = Experience
    template_name = 'account/experience_detail.html'
    context_object_name = 'experience'

    def get(self, request, *args, **kwargs):
        experience = self.get_object()
        data = {
            'id': experience.id,
            'company': experience.company,
            'title': experience.title,
            'location': experience.location,
            'description': experience.description,
            'from_date': experience.from_date,
            'to_date': experience.to_date,
            'current': experience.current,
        }
        return JsonResponse(data)

class ExperienceDeleteView(LoginRequiredMixin, DeleteView):
    model = Experience
    success_url = reverse_lazy('add_experience')

# education related views
class EducationCreateView(LoginRequiredMixin, CreateView):
    model = Education
    form_class = EducationForm
    template_name = 'account/add_education.html'
    success_message = 'Education created successfully!'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = self.request.user
        kwargs['initial'] = {'profile': user.profile}
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['educations'] = Education.objects.filter(profile=self.request.user.profile)
        
        # Add the newly created education to the context
        if self.object:
            education = self.object.pk
            context['education'] = education
        
        return context

    def get_success_url(self):
        return reverse_lazy('add_education')
    
    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        return super().form_valid(form)
    
class EducationUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Education
    form_class = EducationForm
    template_name = 'account/edit_education.html'
    success_message = 'Education updated successfully!'

    def get_success_url(self):
        return reverse_lazy('add_education')  # Consider redirecting to a more relevant page

    def form_valid(self, form):
        form.save()  
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        education = self.get_object()  
        context['education'] = education
        return context

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.kwargs['pk'])

class EducationDetailView(LoginRequiredMixin, DetailView):
    model = Education
    template_name = 'account/education_detail.html'
    context_object_name = 'education'

    def get(self, request, *args, **kwargs):
        education = self.get_object()
        data = {
            'id': education.id,
            'school': education.school,
            'fieldofstudy': education.fieldofstudy,
            'degree': education.degree,
            'description': education.description,
            'from_date': education.from_date,
            'to_date': education.to_date,
            'current': education.current,
        }
        return JsonResponse(data)

class EducationDeleteView(LoginRequiredMixin, DeleteView):
    model = Education
    success_url = reverse_lazy('add_education')
