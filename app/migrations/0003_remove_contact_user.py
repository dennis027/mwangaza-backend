# Generated by Django 3.2.5 on 2022-01-11 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_contact'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='user',
        ),
    ]