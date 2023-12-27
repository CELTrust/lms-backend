import datetime
from typing import List, Literal, Self

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


class QuestionAttemptIn(Schema):
    school_id: int
    gr_number: str
    sync_device_id: str
    question_id: int
    is_correct: bool
    updated_at: datetime.datetime

class SyncQuestionAttemptOut(Schema):
    school_id: int
    gr_number: str

    question_id: int
    result: Literal["success", "error"]
    detail: str = ""

    @classmethod
    def create_success(cls, school_id: int, question_id: int, gr_number: int):
        return cls(
            school_id=school_id,
            question_id=question_id,
            gr_number=gr_number,
            result="success",
        )

    @classmethod
    def create_error(cls, school_id: int, question_id: int, gr_number: int, detail: str):
        return cls(
            school_id=school_id,
            question_id=question_id,
            gr_number=gr_number,
            result="error",
            detail=detail,
        )

class SyncQuestionAttemptsOut(Schema):
    results: List[SyncQuestionAttemptOut]


class SyncQuestionAttemptsIn(Schema):
    data: List[QuestionAttemptIn]


class CELUserIn(Schema):
    school_id: int
    gr_number: str
    name: str

class SyncCELUsersIn(Schema):

    data: List[CELUserIn]


class SyncCELUserOut(Schema):
    gr_number: str
    result: Literal["success", "error"]
    detail: str = ""

    @classmethod
    def create_success(cls, gr_number) -> Self:
        return cls(gr_number=gr_number, result="success")

    @classmethod
    def create_error(cls, gr_number, detail) -> Self:
        return cls(gr_number=gr_number, result="error", detail=detail)


class SyncCELUsersOut(Schema):
    results: List[SyncCELUserOut]
