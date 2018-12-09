# Generated by Django 2.1.4 on 2018-12-09 21:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djangotwitter', '0002_remove_notification_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='follower',
        ),
        migrations.AddField(
            model_name='notification',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='djangotwitter.TwitterUser'),
        ),
        migrations.AddField(
            model_name='notification',
            name='body',
            field=models.TextField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='notification',
            name='metioned_by',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]