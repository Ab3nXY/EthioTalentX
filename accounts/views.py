from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ProfileForm, ExperienceForm, EducationForm, ExperienceFormSet
from .models import Profile, Skill, Education, Experience
from django.forms import formset_factory

# Create your views here.
def index(request):
  return render(request, 'index.html')

@login_required
def profile(request):
    """
    Renders the profile view with a form for profile updates.
    Redirects to the dashboard after successful form submission.
    """

    try:
        profile = Profile.objects.get(user=request.user)  # Assuming user is logged in and has a profile
    except Profile.DoesNotExist:
        # Handle case where profile doesn't exist (e.g., create a new one)
        profile = None
        # ... (Optional: Create a new profile or handle the error differently)

    if request.method == 'POST':
        form = ProfileForm(user=request.user, data=request.POST, files=request.FILES, instance=profile)
        print(f"request: {request.POST}")
        if form.is_valid():
            profile = form.save(commit=True)
            print(f"Skills: {profile.skills}")  # Debugging output
            return redirect('dashboard')
    else:
        form = ProfileForm(user=request.user,instance=profile)

    context = {'profile': profile, 'form': form}
    return render(request, 'account/profile.html', context)

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

    profiles = Profile.objects.all()  # Fetch all profiles
    context = {'profiles': profiles}
    return render(request, 'account/profiles.html', context)

@login_required
def add_experience(request):
    """
    Renders a form for users to create or edit experience data.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: A rendered HTML response containing the form.
    """

    if request.method == 'POST':
        formset = ExperienceFormSet(request.POST)
        if formset.is_valid():
            # Process valid formset data here (save to database, etc.)
            for form in formset:
                form.save(user=request.user)  # Pass the current user to the save method
            return render(request, 'experience_success.html', {'message': 'Experience(s) saved successfully!'})
    else:
        formset = ExperienceFormSet()

    context = {'formset': formset}
    return render(request, 'account/add_experience.html', context)

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
