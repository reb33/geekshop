# Generated by Django 3.2 on 2021-12-21 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0006_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='languages',
            field=models.CharField(blank=True, max_length=50, verbose_name='языки'),
        ),
    ]