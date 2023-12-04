from django.contrib import admin
from .models import Course, Lesson, Quiz, Question, Option

# Register your models here.
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Option)
