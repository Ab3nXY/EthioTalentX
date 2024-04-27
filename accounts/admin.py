from django.contrib import admin
from .models import Profile,Skill, Education, Experience

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Profile._meta.fields]

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Experience._meta.fields]

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Education._meta.fields]
