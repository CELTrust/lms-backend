from django.db import models
from common import constants
from product.models import Option, Question, Quiz, Lesson, Course, School

class CELUser(models.Model):
    name = models.CharField(max_length=255)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    gr_num = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("school", "gr_num"),)

    def __str__(self) -> str:
        return "< {} >".format(self.name)


class CourseAttempt(models.Model):
    user = models.ForeignKey(CELUser, on_delete=models.CASCADE, related_name="course_attempts")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="attempts")

    status = models.CharField(max_length=64, choices=constants.STATUSES)
    score = models.IntegerField(default=0)
    sync_device_id = models.CharField(max_length=255) ## this will be used to determine which device was used to create / update this entry

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("user", "course"),)

class LessonAttempt(models.Model):
    user = models.ForeignKey(CELUser, on_delete=models.CASCADE, related_name="lesson_attempts")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="attempts")

    status = models.CharField(max_length=64, choices=constants.STATUSES)
    score = models.IntegerField(default=0)
    sync_device_id = models.CharField(max_length=255) ## this will be used to determine which device was used to create / update this entry

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("user", "lesson"),)


class ProjectUploadAttempt(models.Model):
    user = models.ForeignKey(CELUser, on_delete=models.CASCADE, related_name="project_upload_attempts")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="project_upload_attempts")

    file = models.FileField()
    size = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("user", "course"))


# Answers
class QuizAttempt(models.Model):
    user = models.ForeignKey(CELUser, on_delete=models.CASCADE, related_name="quiz_attempts")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="attempts")

    status = models.CharField(max_length=64, choices=constants.STATUSES)
    score = models.IntegerField(default=0)
    sync_device_id = models.CharField(max_length=255, blank=True, null=True) ## this will be used to determine which device was used to create / update this entry

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# TODO: maybe this can be removed in the first iteration?
class QuestionAttempt(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="answers")
    user = models.ForeignKey(CELUser, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    options = models.ManyToManyField(Option)
    is_correct = models.BooleanField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
