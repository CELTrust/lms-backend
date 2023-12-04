from django.contrib import admin
from .models import School, CELUser, QuizAttempt, LessonAttempt, CourseAttempt

# Register your models here.
admin.site.register(School)
admin.site.register(CELUser)
admin.site.register(QuizAttempt)
admin.site.register(LessonAttempt)
admin.site.register(CourseAttempt)
