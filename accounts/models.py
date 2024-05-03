from django.db import models
from django.contrib.auth.models import User

OCCUPATION_CHOICES = [
    ('Developer', 'Developer'),
    ('Intern', 'Intern'),
    ('Other', 'Other'),
    ('Django Developer', 'Django Developer'),
    ('Fullstack Developer', 'Fullstack Developer'),
    ('MERN Stack Developer', 'MERN Stack Developer'),
    ('Front-End Developer', 'Front-End Developer'),
    ('Back-End Developer', 'Back-End Developer'),
    ('Software Engineer', 'Software Engineer'),
    ('Data Scientist', 'Data Scientist'),
    ('Machine Learning Engineer', 'Machine Learning Engineer'),
]

SKILLS_CHOICES = [
    ('HTML', 'HTML'),
    ('CSS', 'CSS'),
    ('JavaScript', 'JavaScript'),
    ('React', 'React'),
    ('Node.js', 'Node.js'),
    ('Angular', 'Angular'),
    ('Vue.js', 'Vue.js'),
    ('Bootstrap', 'Bootstrap'),
    ('jQuery', 'jQuery'),
    ('Django', 'Django'),
    ('Flask', 'Flask'),
    ('Python', 'Python'),
    ('Java', 'Java'),
    ('C++', 'C++'),
    ('C#', 'C#'),
    ('Ruby', 'Ruby'),
    ('PHP', 'PHP'),
    ('SQL', 'SQL'),
    ('MongoDB', 'MongoDB'),
    ('PostgreSQL', 'PostgreSQL'),
    ('Git', 'Git'),
    ('Amazon Web Services (AWS)', 'Amazon Web Services (AWS)'),
    ('Microsoft Azure', 'Microsoft Azure'),
    ('Google Cloud Platform (GCP)', 'Google Cloud Platform (GCP)'),
    ('Docker', 'Docker'),
    ('Kubernetes', 'Kubernetes'),
    ('TensorFlow', 'TensorFlow'),
    ('PyTorch', 'PyTorch'),
    ('Scikit-learn', 'Scikit-learn'),
    ('Pandas', 'Pandas'),
    ('NumPy', 'NumPy'),
    ('Matplotlib', 'Matplotlib'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=100, blank=True, null=True, default='')
    website = models.URLField(max_length=200, blank=True, default='')
    location = models.CharField(max_length=100, blank=True, null=True, default='')
    bio = models.TextField(blank=True, null=True, default='')
    githubusername = models.CharField(max_length=100, blank=True, null=True, default='')
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(default="profile_pics/default.jpg", upload_to='profile_pics', blank=True)
    occupation = models.CharField(max_length=100, choices=OCCUPATION_CHOICES, blank=False, default='')
    skills = models.ManyToManyField('Skill', related_name='profiles', blank=False)

    def __str__(self):
        return f'{self.user.username} Profile'

class Skill(models.Model):
    name = models.CharField(max_length=100, choices=SKILLS_CHOICES)

    def __str__(self):
        return self.name

class Experience(models.Model):
    profile = models.ForeignKey(Profile, related_name='experience', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default='')
    company = models.CharField(max_length=100, default='')
    location = models.CharField(max_length=100, blank=True, null=True, default='')
    from_date = models.DateField()
    to_date = models.DateField(blank=True, null=True)
    current = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True, default='')

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
