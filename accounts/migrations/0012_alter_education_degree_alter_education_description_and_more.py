# Generated by Django 5.0.4 on 2024-05-06 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_alter_profile_occupation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='degree',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='education',
            name='description',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='education',
            name='fieldofstudy',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='education',
            name='school',
            field=models.CharField(default='', max_length=100),
        ),
    ]