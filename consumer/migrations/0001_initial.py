# Generated by Django 4.2.7 on 2023-12-28 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CELUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('gr_number', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.school')),
            ],
            options={
                'unique_together': {('school', 'gr_number')},
            },
        ),
        migrations.CreateModel(
            name='QuestionAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('started', 'started'), ('finished', 'finished')], default='started', max_length=64)),
                ('score', models.IntegerField(default=0)),
                ('sync_device_id', models.CharField(max_length=255)),
                ('started_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='product.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='consumer.celuser')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProjectUploadAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('started', 'started'), ('finished', 'finished')], default='started', max_length=64)),
                ('score', models.IntegerField(default=0)),
                ('sync_device_id', models.CharField(max_length=255)),
                ('started_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('file_path', models.CharField(max_length=255)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_upload_attempts', to='product.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_upload_attempts', to='consumer.celuser')),
            ],
            options={
                'unique_together': {('user', 'course')},
            },
        ),
        migrations.CreateModel(
            name='LessonAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('started', 'started'), ('finished', 'finished')], default='started', max_length=64)),
                ('score', models.IntegerField(default=0)),
                ('sync_device_id', models.CharField(max_length=255)),
                ('started_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attempts', to='product.lesson')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson_attempts', to='consumer.celuser')),
            ],
            options={
                'unique_together': {('user', 'lesson')},
            },
        ),
        migrations.CreateModel(
            name='CourseAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('started', 'started'), ('finished', 'finished')], default='started', max_length=64)),
                ('score', models.IntegerField(default=0)),
                ('sync_device_id', models.CharField(max_length=255)),
                ('started_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attempts', to='product.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_attempts', to='consumer.celuser')),
            ],
            options={
                'unique_together': {('user', 'course')},
            },
        ),
    ]
