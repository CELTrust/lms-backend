from django.db import models
from common.models import Tracker, DescCommonFields

class Course(DescCommonFields):
    pass


class Lesson(DescCommonFields):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True) # TODO: remove blank and null check later
    video_link = models.URLField()
    presentation_link = models.URLField()
    project_description = models.TextField()


class Quiz(Tracker):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "Quiz for lesson < {} >".format(self.lesson.name)

class Question(Tracker):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()

    def __str__(self) -> str:
        return "{}".format(self.text)

class Option(Tracker):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.text
