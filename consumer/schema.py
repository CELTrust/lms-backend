import datetime
from typing import List, Literal

from ninja import Schema


class CourseAttemptIn(Schema):
    school_id: int
    gr_number: str
    course_id: int
    status: Literal["started", "finished"]
    sync_device_id: str
    score: int = 0
    updated_at: datetime.datetime


class SyncCourseAttemptsIn(Schema):
    data: List[CourseAttemptIn]


class SyncCourseAttemptOut(Schema):
    school_id: int
    course_id: int
    gr_number: str
    result: Literal["success", "error"]
    detail: str = ""

    @classmethod
    def create_success(cls, school_id: int, course_id: int, gr_number: int):
        return cls(
            school_id=school_id,
            course_id=course_id,
            gr_number=gr_number,
            result="success",
        )

    @classmethod
    def create_error(cls, school_id: int, course_id: int, gr_number: int, detail: str):
        return cls(
            school_id=school_id,
            course_id=course_id,
            gr_number=gr_number,
            result="error",
            detail=detail,
        )


class SyncCourseAttemptsOut(Schema):
    results: List[SyncCourseAttemptOut]


class LessonAttemptIn(Schema):
    school_id: int
    gr_number: str
    lesson_id: int
    status: Literal["started", "finished"]
    sync_device_id: str
    score: int = 0
    updated_at: datetime.datetime


class SyncLessonAttemptsIn(Schema):
    data: List[LessonAttemptIn]


class SyncLessonAttemptOut(Schema):
    school_id: int
    lesson_id: int
    gr_number: str
    result: Literal["success", "error"]
    detail: str = ""

    @classmethod
    def create_success(cls, school_id: int, lesson_id: int, gr_number: int):
        return cls(
            school_id=school_id,
            lesson_id=lesson_id,
            gr_number=gr_number,
            result="success",
        )

    @classmethod
    def create_error(cls, school_id: int, lesson_id: int, gr_number: int, detail: str):
        return cls(
            school_id=school_id,
            lesson_id=lesson_id,
            gr_number=gr_number,
            result="error",
            detail=detail,
        )


class SyncLessonAttemptsOut(Schema):
    results: List[SyncLessonAttemptOut]


class QuestionAttemptSchemaIn(Schema):
    question_id: int
    selected_options: List[int] = []
    is_correct: bool


class QuizAttemptSchemaIn(Schema):
    school_id: int
    gr_number: str
    quiz_id: int
    sync_device_id: str
    question_attempts: List[QuestionAttemptSchemaIn]
    updated_at: datetime.datetime


class SyncQuizAttemptSchema(Schema):
    data: List[QuizAttemptSchemaIn]


class SyncQuizAttemptOut(Schema):
    school_id: int
    quiz_id: int
    gr_number: str
    result: Literal["success", "error"]
    detail: str = ""

    @classmethod
    def create_success(cls, school_id: int, quiz_id: int, gr_number: int):
        return cls(
            school_id=school_id,
            quiz_id=quiz_id,
            gr_number=gr_number,
            result="success",
        )

    @classmethod
    def create_error(cls, school_id: int, quiz_id: int, gr_number: int, detail: str):
        return cls(
            school_id=school_id,
            quiz_id=quiz_id,
            gr_number=gr_number,
            result="error",
            detail=detail,
        )


class SyncQuizAttemptsOut(Schema):
    results: List[SyncQuizAttemptOut]
