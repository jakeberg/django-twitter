# Generated by Django 2.1.4 on 2018-12-09 21:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djangotwitter', '0004_auto_20181209_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='metioned_by',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='djangotwitter.Tweet'),
        ),
    ]