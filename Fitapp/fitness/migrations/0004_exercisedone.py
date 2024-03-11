# Generated by Django 4.2.10 on 2024-03-11 18:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fitness', '0003_exercisebook_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExerciseDone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.IntegerField()),
                ('date', models.DateField()),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitness.exercisebook')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]