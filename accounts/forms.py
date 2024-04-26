from django import forms
from .models import Profile, Experience, Education, OCCUPATION_CHOICES, SKILLS_CHOICES
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, Submit

class ProfileForm(forms.ModelForm):
    occupation = forms.MultipleChoiceField(choices=OCCUPATION_CHOICES, widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    skills = forms.MultipleChoiceField(choices=SKILLS_CHOICES, widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    class Meta:
        model = Profile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-control'
        self.helper.layout = Layout(
            Fieldset(
                'Profile Information',

                Row(
                    Column('status', css_class='col-md-6'),
                    Column('location', css_class='col-md-6'),
                    
                ),                
                Row(
                    Column('company', css_class='col-md-6'),
                    Column('website', css_class='col-md-6'),
                ),
                Row(
                    Column('skills', css_class='col-md-12'),
                ),
                Row(
                    Column('bio', css_class='col-md-12'),
                ),
                Row(
                    Column('githubusername', css_class='col-md-6'),
                ),
            ),
            'experience',  # Assuming you have a separate formset for experience
            'education',  # Assuming you have a separate formset for education
            'social',
            'date',
            Submit('submit', 'Update Profile', css_class='btn btn-primary')
        )

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = '__all__'

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = '__all__'