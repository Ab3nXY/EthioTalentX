# Generated by Django 5.0.4 on 2024-05-24 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='last_message_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
