from django.contrib import admin

from .models import (CELUser, CourseAttempt, LessonAttempt, QuestionAttempt,
                     School)

# Register your models here.
admin.site.register(School)
admin.site.register(CELUser)
admin.site.register(LessonAttempt)
admin.site.register(CourseAttempt)
admin.site.register(QuestionAttempt)
