from django.contrib import admin

from .models import Course, Lesson, Option, Question, School

admin.site.register(Lesson)
admin.site.register(School)

class OptionAdmin(admin.StackedInline):
    model = Option


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionAdmin,]

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)
