from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ProfileForm
from .models import Profile

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
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to your desired dashboard URL pattern name
    else:
        form = ProfileForm(instance=profile)

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
