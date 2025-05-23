# Generated by Django 4.2.15 on 2024-08-26 10:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elearn_app', '0003_alter_profile_user_image_course'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material', models.FileField(upload_to='course_materials')),
                ('uploaded_at', models.DateTimeField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elearn_app.course')),
            ],
        ),
    ]
