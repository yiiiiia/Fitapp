# Generated by Django 4.1 on 2024-03-03 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='age',
            field=models.PositiveIntegerField(default=0, verbose_name='Age'),
        ),
    ]
