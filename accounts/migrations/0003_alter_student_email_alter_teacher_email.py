# Generated by Django 5.1.2 on 2024-10-31 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_teacher_subject_student_address_student_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]