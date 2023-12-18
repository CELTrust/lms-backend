import datetime

from django.db import models
from typing_extensions import Self

from common import constants
from product.models import Course, Lesson, Option, Question, Quiz, School


class CELUser(models.Model):
    name = models.CharField(max_length=255)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    gr_number = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("school", "gr_number"),)

    def __str__(self) -> str:
        return "< {} >".format(self.name)

    @classmethod
    def exists(cls, id) -> bool:
        return cls.objects.filter(id=id).exists()


class CourseAttempt(models.Model):
    user = models.ForeignKey(
        CELUser, on_delete=models.CASCADE, related_name="course_attempts"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="attempts"
    )

    status = models.CharField(
        max_length=64,
        choices=constants.StatusChoices.choices(),
        default=constants.STATUS_STARTED,
    )
    score = models.IntegerField(default=0)
    sync_device_id = models.CharField(
        max_length=255
    )  ## this will be used to determine which device was used to create / update this entry

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def can_update(self, updated_at) -> bool:
        return not self.has_finished() and updated_at > self.updated_at

    def has_finished(self) -> bool:
        return self.status == constants.STATUS_FINISHED

    @classmethod
    def exists(cls, id) -> bool:
        return cls.objects.filter(id=id).exists()

    class Meta:
        unique_together = (("user", "course"),)

    @classmethod
    def get_by_user_course(cls, user_id, course_id) -> Self:
        return cls.objects.filter(user_id=user_id, course_id=course_id).first()

    @classmethod
    def create_attempt(
        cls,
        user_id: int,
        course_id: int,
        score: int,
        sync_device_id: int,
        updated_at: datetime.datetime,
    ) -> Self:
        obj = cls.objects.create(
            user_id=user_id,
            course_id=course_id,
            status=constants.STATUS_STARTED,
            score=score,
            sync_device_id=sync_device_id,
            created_at=updated_at,
            updated_at=updated_at,
        )
        return obj

    def update_attempt(
        self, sync_device_id: str, score: int, updated_at: datetime.datetime
    ) -> Self:
        self.sync_device_id = sync_device_id
        self.score = score
        self.updated_at = updated_at
        self.save()
        return self


class LessonAttempt(models.Model):
    user = models.ForeignKey(
        CELUser, on_delete=models.CASCADE, related_name="lesson_attempts"
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="attempts"
    )

    status = models.CharField(max_length=64, choices=constants.StatusChoices)
    score = models.IntegerField(default=0)
    sync_device_id = models.CharField(
        max_length=255
    )  ## this will be used to determine which device was used to create / update this entry

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def can_update(self, updated_at) -> bool:
        return not self.has_finished() and updated_at > self.updated_at

    def has_finished(self) -> bool:
        return self.status == constants.STATUS_FINISHED

    @classmethod
    def exists(cls, id) -> bool:
        return cls.objects.filter(id=id).exists()

    @classmethod
    def get_by_user_lesson(cls, user_id, lesson_id) -> Self:
        return LessonAttempt.objects.filter(
            user_id=user_id, lesson_id=lesson_id
        ).first()

    @classmethod
    def create_attempt(
        cls,
        user_id: int,
        lesson_id: int,
        score: int,
        sync_device_id: int,
        updated_at: datetime.datetime,
    ) -> Self:
        obj = cls.objects.create(
            user_id=user_id,
            lesson_id=lesson_id,
            status=constants.STATUS_STARTED,
            score=score,
            sync_device_id=sync_device_id,
            created_at=updated_at,
            updated_at=updated_at,
        )
        return obj

    def update_attempt(
        self, sync_device_id: str, score: int, updated_at: datetime.datetime
    ) -> Self:
        self.sync_device_id = sync_device_id
        self.score = score
        self.updated_at = updated_at
        self.save()
        return self

    class Meta:
        unique_together = (("user", "lesson"),)


class ProjectUploadAttempt(models.Model):
    user = models.ForeignKey(
        CELUser, on_delete=models.CASCADE, related_name="project_upload_attempts"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="project_upload_attempts"
    )

    file = models.FileField()
    size = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def exists(cls, id) -> bool:
        return cls.objects.filter(id=id).exists()

    class Meta:
        unique_together = ("user", "course")


# Answers
class QuizAttempt(models.Model):
    user = models.ForeignKey(
        CELUser, on_delete=models.CASCADE, related_name="quiz_attempts"
    )
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="attempts")

    status = models.CharField(max_length=64, choices=constants.STATUSES)
    score = models.IntegerField(default=0)
    sync_device_id = models.CharField(
        max_length=255, blank=True, null=True
    )  ## this will be used to determine which device was used to create / update this entry

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def exists(cls, id) -> bool:
        return cls.objects.filter(id=id).exists()

    def has_finished(self) -> bool:
        return self.status == constants.STATUS_FINISHED

    def can_update(self, updated_at) -> bool:
        return not self.has_finished() and updated_at > self.updated_at


class QuestionAttempt(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="answers")
    user = models.ForeignKey(CELUser, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    options = models.ManyToManyField(Option)
    is_correct = models.BooleanField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def exists(cls, id) -> bool:
        return cls.objects.filter(id=id).exists()
