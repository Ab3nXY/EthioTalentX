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
        fields = '__all__'


    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['user'].initial = self.user.username
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                Row(
                    Column('user', css_class='col-md-6'),
                    Column('occupation', css_class='col-md-6'),
                ),
                Row(
                    Column('location', css_class='col-md-6'),
                    Column('company', css_class='col-md-6'),
                ),
                Row(
                    Column('website', css_class='col-md-6'),
                    Column('image', css_class='col-md-6'),  # Include image field
                ),
                'bio',
                'skills',
                Row(
                    Column('githubusername', css_class='col-md-6'),
                ),
            ),
            'social',
            'date',
            Submit('submit', 'Update Profile', css_class='btn btn-primary'),
        )

    def clean_user(self):
        return self.user  # Make sure the user field retains the current user's value

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
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
