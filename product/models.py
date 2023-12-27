import random
from collections.abc import Iterable

from django.db import models
from django.utils.text import slugify

from common.models import CommonFields, DescCommonFields, Tracker


class School(CommonFields):
    pass


class Course(DescCommonFields):
    pass

class Lesson(DescCommonFields):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    video_link = models.URLField()
    presentation_link = models.URLField()

    has_project = models.BooleanField()
    project_description = models.TextField()

    def __str__(self) -> str:
        return "< {} >".format(self.name)


class Question(Tracker):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()

    def __str__(self) -> str:
        return "{}".format(self.text)


class Option(Tracker):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.text
