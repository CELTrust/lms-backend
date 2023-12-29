import datetime
import os
from uuid import uuid1

from django.db import models
from django.shortcuts import get_object_or_404
from typing_extensions import Self

from common import constants
from common.models import AttemptTracker, Tracker
from consumer.exceptions import ErrFileNotUploaded
from lms.s3 import (UploadDataSchema, create_presigned_url_get,
                    create_presigned_url_post, does_file_exist)
from product.models import Course, Lesson, Question, School


class CELUser(Tracker):
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

    @classmethod
    def create(cls, school_id, name, gr_number) -> Self:
        return cls.objects.create(school_id=school_id, name=name, gr_number=gr_number)


class CourseAttempt(AttemptTracker):
    user = models.ForeignKey(
        CELUser, on_delete=models.CASCADE, related_name="course_attempts"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="attempts"
    )

    class Meta:
        unique_together = (("user", "course"),)

    @classmethod
    def get_by_user_course(cls, user_id, course_id) -> Self:
        return cls.objects.filter(user_id=user_id, course_id=course_id).first()

    @classmethod
    def create_attempt(cls, user_id: int, course_id: int, score: int, sync_device_id: int,
                       updated_at: datetime.datetime) -> Self:
        obj = cls.objects.create(user_id=user_id, course_id=course_id, status=constants.STATUS_STARTED, score=score,
                                 ync_device_id=sync_device_id, started_at=updated_at, updated_at=updated_at)
        return obj

    def update_attempt(
        self, sync_device_id: str, score: int, updated_at: datetime.datetime
    ) -> Self:
        self.sync_device_id = sync_device_id
        self.score = score
        self.updated_at = updated_at
        self.save()
        return self


class LessonAttempt(AttemptTracker):
    user = models.ForeignKey(
        CELUser, on_delete=models.CASCADE, related_name="lesson_attempts"
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="attempts"
    )

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
            started_at=updated_at,
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


class ProjectUploadAttempt(AttemptTracker):
    user = models.ForeignKey(CELUser, on_delete=models.CASCADE, related_name="project_upload_attempts")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="project_upload_attempts")

    file_path = models.CharField(max_length=255)

    @classmethod
    def exists(cls, id) -> bool:
        return cls.objects.filter(id=id).exists()

    class Meta:
        unique_together = ("user", "course")

    @classmethod
    def create_new(cls, user_id: int, course_id: int, file: str, updated_at: datetime.datetime) -> Self:
        filename, ext = os.path.splitext(file)
        uniq = str(uuid1())[-5:]
        path = "/user/{user_id}/course/{course_id}/{filename}-{uniq}{ext}".format(
            user_id=user_id, course_id=course_id, filename=filename, ext=ext, uniq=uniq)

        return cls.objects.create(user_id=user_id, course_id=course_id, file_path=path,
                                  started_at=updated_at, updated_at=updated_at, status=constants.STATUS_STARTED)

    @property
    def upload_url(self) -> UploadDataSchema:
        return create_presigned_url_post(file_path=self.file_path)

    @property
    def download_url(self):
        return create_presigned_url_get(file_path=self.file_path)

    def does_file_exist(self) -> bool:
        return does_file_exist(self.file_path)

    @classmethod
    def mark_finished(cls, id: int) -> Self:
        attempt = get_object_or_404(cls, id=id)
        if not attempt.does_file_exist():
            raise ErrFileNotUploaded

        attempt.updated_at = datetime.datetime.now()
        attempt.status = constants.STATUS_FINISHED
        attempt.save()
        return attempt


# Answers
class QuestionAttempt(AttemptTracker):
    user = models.ForeignKey(CELUser, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")

    @classmethod
    def create_attempt(cls, user_id: int, question_id: int, score: int, sync_device_id: int, updated_at: datetime.datetime) -> Self:
        return cls.objects.create(user_id=user_id, question_id=question_id,
                                  sync_device_id=sync_device_id, updated_at=updated_at, started_at=updated_at,
                                  status=constants.STATUS_FINISHED, score=score)

    def update_attempt(self, score: int, sync_device_id: int, updated_at: datetime.datetime) -> Self:
        self.score = score
        self.sync_device_id = sync_device_id
        self.updated_at = updated_at
        self.status = constants.STATUS_FINISHED
        self.save()
        return self

    # TODO: add option_ids and corresponding validation
    @classmethod
    def exists(cls, id) -> bool:
        return cls.objects.filter(id=id).exists()
