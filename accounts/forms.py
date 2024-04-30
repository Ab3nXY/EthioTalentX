from django import forms
from .models import Profile, Experience, Education, OCCUPATION_CHOICES, SKILLS_CHOICES, Skill
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, Submit
from django.contrib.auth.models import User


class ProfileForm(forms.ModelForm):
    occupation = forms.ChoiceField(choices=OCCUPATION_CHOICES, initial='developer', widget=forms.Select(attrs={'class': 'form-select'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'blank': True}))
    skills = forms.MultipleChoiceField(choices=SKILLS_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-select'}))

    class Meta:
        model = Profile
        exclude = ['user']  # Exclude the user field from the form

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
        fields = '__all__'  # Include all fields for editing

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = '__all__'
