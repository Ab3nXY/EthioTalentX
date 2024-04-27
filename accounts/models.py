from django.db import models
from django.contrib.auth.models import User

OCCUPATION_CHOICES = [
    ('developer', 'Developer'),
    ('intern', 'Intern'),
    ('other', 'Other'),
    ('django_developer', 'Django Developer'),
    ('fullstack_developer', 'Fullstack Developer'),
    ('mern_stack_developer', 'MERN Stack Developer'),
    ('front_end_developer', 'Front-End Developer'),
    ('back_end_developer', 'Back-End Developer'),
    ('software_engineer', 'Software Engineer'),
    ('data_scientist', 'Data Scientist'),
    ('machine_learning_engineer', 'Machine Learning Engineer'),
]

SKILLS_CHOICES = [
    ('html', 'HTML'),
    ('css', 'CSS'),
    ('javascript', 'JavaScript'),
    ('react', 'React'),
    ('node', 'Node.js'),
    ('angular', 'Angular'),
    ('vue', 'Vue.js'),
    ('bootstrap', 'Bootstrap'),
    ('jquery', 'jQuery'),
    ('django', 'Django'),
    ('flask', 'Flask'),
    ('python', 'Python'),
    ('java', 'Java'),
    ('c_plus_plus', 'C++'),
    ('c_sharp', 'C#'),
    ('ruby', 'Ruby'),
    ('php', 'PHP'),
    ('sql', 'SQL'),
    ('mongodb', 'MongoDB'),
    ('postgresql', 'PostgreSQL'),
    ('git', 'Git'),
    ('aws', 'Amazon Web Services (AWS)'),
    ('azure', 'Microsoft Azure'),
    ('gcp', 'Google Cloud Platform (GCP)'),
    ('docker', 'Docker'),
    ('kubernetes', 'Kubernetes'),
    ('tensorflow', 'TensorFlow'),
    ('pytorch', 'PyTorch'),
    ('scikit_learn', 'Scikit-learn'),
    ('pandas', 'Pandas'),
    ('numpy', 'NumPy'),
    ('matplotlib', 'Matplotlib'),
]



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    githubusername = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(default="profile_pics/default.jpg", upload_to='profile_pics')
    occupation = models.CharField(max_length=100, choices=OCCUPATION_CHOICES, blank=True, null=True)
    skills = models.ManyToManyField('Skill', related_name='profiles', blank=False)

    def __str__(self):
        return f'{self.user.username} Profile'

class Skill(models.Model):
    name = models.CharField(max_length=100, choices=SKILLS_CHOICES)

    def __str__(self):
        return self.name

class Experience(models.Model):
    profile = models.ForeignKey(Profile, related_name='experience', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True, null=True)
    from_date = models.DateField()
    to_date = models.DateField(blank=True, null=True)
    current = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.title} at {self.company}'

class Education(models.Model):
    profile = models.ForeignKey(Profile, related_name='education', on_delete=models.CASCADE)
    school = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    fieldofstudy = models.CharField(max_length=100)
    from_date = models.DateField()
    to_date = models.DateField(blank=True, null=True)
    current = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.degree} in {self.fieldofstudy} at {self.school}'
    
    class Meta:
        app_label = 'accounts'
