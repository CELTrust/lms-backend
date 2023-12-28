import random
import string

from django.db import models

from common.models import CommonFields, DescCommonFields, Tracker


class School(CommonFields):
    unique_code = models.CharField(max_length=10, editable=False, unique=True)

    @classmethod
    def generate_unique_code(cls) -> str:
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if cls.objects.filter(unique_code=code).exists():
            return cls.generate_unique_code()
        return code


    def save(self, *args, **kwargs) -> None:
        if not self.unique_code:
            self.unique_code = self.__class__.generate_unique_code()
        return super().save(*args, **kwargs)


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
