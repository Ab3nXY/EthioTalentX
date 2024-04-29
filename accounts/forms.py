from django import forms
from .models import Profile, Experience, Education, OCCUPATION_CHOICES, SKILLS_CHOICES, Skill
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, Submit
from django.contrib.auth.models import User
from django.forms import formset_factory

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

    def save(self, user=None, commit=True):
        profile = super().save(commit=False)
        if commit:
            if user:
                # Update user-related fields if provided
                if self.cleaned_data['first_name'] != user.first_name:
                    user.first_name = self.cleaned_data['first_name']
                if self.cleaned_data['last_name'] != user.last_name:
                    user.last_name = self.cleaned_data['last_name']
                user.save()
            profile.save()
            self.save_m2m()
        return profile

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['title', 'company', 'location', 'description', 'from_date', 'to_date']

        widgets = {
            'start_date': forms.SelectDateWidget(),
            'end_date': forms.SelectDateWidget(),
        }

    def __init__(self, *args, **kwargs):
        super(ExperienceForm, self).__init__(*args, **kwargs)
        self.fields['from_date'].label = "Start Date"
        self.fields['to_date'].label = "End Date"



        # Add custom styling using crispy forms or HTML classes
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'title',
            'company',
            'location',
            'description',
            'from_date',
            'to_date',
        )

ExperienceFormSet = formset_factory(ExperienceForm, extra=1)

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = '__all__'
