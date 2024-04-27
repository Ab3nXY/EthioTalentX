from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ProfileForm
from .models import Profile, Skill, Education, Experience

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
  return render(request, 'account/profiles.html')

@login_required
def add_experience(request):
  return render(request, 'account/add_experience.html')

@login_required
def add_education(request):
  return render(request, 'account/add_education.html')
