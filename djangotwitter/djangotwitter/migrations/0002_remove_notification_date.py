# Generated by Django 2.1.4 on 2018-12-09 21:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangotwitter', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='date',
        ),
    ]