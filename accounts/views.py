from django.shortcuts import render
from .models import Profile
from .forms import ProfileForm

# Create your views here.
def index(request):
  return render(request, 'index.html')

def profile(request):
    profile = Profile.objects.get(user=request.user)  # Assuming user is logged in and has a profile
    form = ProfileForm(instance=profile)
    return render(request, 'account/profile.html', {'profile': profile, 'form': form})

def dashboard(request):
  return render(request, 'account/dashboard.html')