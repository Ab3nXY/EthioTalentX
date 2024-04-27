from django import forms
from .models import Profile, Experience, Education, OCCUPATION_CHOICES, SKILLS_CHOICES
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, Submit

class ProfileForm(forms.ModelForm):
    user = forms.CharField(widget=forms.TextInput(attrs={'readonly': True, 'class': 'form-control'}))
    occupation = forms.ChoiceField(choices=OCCUPATION_CHOICES, initial='developer', widget=forms.Select(attrs={'class': 'form-select'}))
    skills = forms.MultipleChoiceField(choices=SKILLS_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-select'}))

    class Meta:
        model = Profile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        user_instance = kwargs.pop('user_instance', None)
        super(ProfileForm, self).__init__(*args, **kwargs)
        if user_instance:
            self.fields['user'].initial = user_instance.username
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Profile Information',
                Row(
                    Column('occupation', css_class='col-md-6'),
                    Column('location', css_class='col-md-6'),
                ),
                Row(
                    Column('company', css_class='col-md-6'),
                    Column('website', css_class='col-md-6'),
                ),
                Row(
                    Column('skills', css_class='col-md-12 skill-columns'),
                ),
                Row(
                    Column('bio', css_class='col-md-12'),
                ),
                Row(
                    Column('githubusername', css_class='col-md-6'),
                ),
            ),
            'social',
            'date',
            Submit('submit', 'Update Profile', css_class='btn btn-primary'),
        )

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = '__all__'

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = '__all__'
