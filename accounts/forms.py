from django import forms
from .models import Profile, Experience, Education, OCCUPATION_CHOICES, SKILLS_CHOICES
from crispy_forms.helper import FormHelper


class ProfileForm(forms.ModelForm):
    occupation = forms.ChoiceField(choices=OCCUPATION_CHOICES, initial='developer', widget=forms.Select(attrs={'class': 'form-select'}))
    skills = forms.MultipleChoiceField(choices=SKILLS_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-select'}))

    class Meta:
        model = Profile
        exclude = ['user']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
            self.save_m2m()
        return profile

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        exclude = ['profile']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        exclude = ['profile']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }
