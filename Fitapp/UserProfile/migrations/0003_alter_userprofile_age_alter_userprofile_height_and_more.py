# Generated by Django 4.1 on 2024-03-03 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfile', '0002_alter_userprofile_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='age',
            field=models.PositiveIntegerField(null=True, verbose_name='Age'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='height',
            field=models.FloatField(null=True, verbose_name='Height'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='weight',
            field=models.FloatField(null=True, verbose_name='Weight'),
        ),
    ]
