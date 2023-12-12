# Generated by Django 4.2.7 on 2023-12-12 11:12

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
                ('gr_num', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.school')),
            ],
            options={
                'unique_together': {('school', 'gr_num')},
            },
        ),
        migrations.CreateModel(
            name='QuizAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('started', 'started'), ('finished', 'finished')], max_length=64)),
                ('score', models.IntegerField(default=0)),
                ('sync_device_id', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attempts', to='product.quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_attempts', to='consumer.celuser')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_correct', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('options', models.ManyToManyField(to='product.option')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='product.question')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='product.quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='consumer.celuser')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectUploadAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
                ('size', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
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
                ('status', models.CharField(choices=[('started', 'started'), ('finished', 'finished')], max_length=64)),
                ('score', models.IntegerField(default=0)),
                ('sync_device_id', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
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
                ('status', models.CharField(choices=[('started', 'started'), ('finished', 'finished')], max_length=64)),
                ('score', models.IntegerField(default=0)),
                ('sync_device_id', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attempts', to='product.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_attempts', to='consumer.celuser')),
            ],
            options={
                'unique_together': {('user', 'course')},
            },
        ),
    ]
