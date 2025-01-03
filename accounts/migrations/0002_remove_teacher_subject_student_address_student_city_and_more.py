# Generated by Django 5.1.2 on 2024-10-30 16:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='subject',
        ),
        migrations.AddField(
            model_name='student',
            name='address',
            field=models.CharField(default='N/A', max_length=255),
        ),
        migrations.AddField(
            model_name='student',
            name='city',
            field=models.CharField(default='Unknown', max_length=255),
        ),
        migrations.AddField(
            model_name='student',
            name='student_class',
            field=models.CharField(default='N/A', max_length=255),
        ),
        migrations.AddField(
            model_name='teacher',
            name='address',
            field=models.CharField(default='N/A', max_length=255),
        ),
        migrations.AddField(
            model_name='teacher',
            name='city',
            field=models.CharField(default='N/A', max_length=100),
        ),
        migrations.AddField(
            model_name='teacher',
            name='classes_taught',
            field=models.CharField(default='N/A', max_length=100),
        ),
        migrations.AddField(
            model_name='teacher',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='teacher_pics/'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='subjects',
            field=models.CharField(default='N/A', max_length=255),
        ),
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.EmailField(default='N/A', max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='name',
            field=models.CharField(default='N/A', max_length=100),
        ),
        migrations.AlterField(
            model_name='student',
            name='pin_code',
            field=models.CharField(default='N/A', max_length=6),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='email',
            field=models.EmailField(default='N/A', max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='name',
            field=models.CharField(default='N/A', max_length=100),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='pin_code',
            field=models.CharField(default='N/A', max_length=6),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pin_code', models.CharField(max_length=6)),
                ('is_teacher', models.BooleanField(default=False)),
                ('subjects', models.CharField(blank=True, max_length=255, null=True)),
                ('class_levels', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
