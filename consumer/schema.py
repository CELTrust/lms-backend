import datetime
from ninja import Schema, Field
from typing import List
from product.schema import CourseSchema, LessonSchema, QuizSchema

class CreateCourseAttemptIn(Schema):
    course_id: int
    user_id: int

class CreateLessonAttemptIn(Schema):
    user_id: int
    lesson_id: int

class CreateQuizAttemptIn(Schema):
    user_id: int
    quiz_id: int

class AnswerIn(Schema):
    question_id: int
    is_correct: bool

class UpdateQuizAttemptIn(Schema):
    user_id: int
    answers: List[AnswerIn]

class CELUserSchema(Schema):
    name: str
    school: Field(None, alias="school.name")
    rollnum: str

class CourseAttemptSchema(Schema):
    id: int
    user: CELUserSchema
    course: CourseSchema
    status: str
    score: str
    started_at: datetime.datetime
    finished_at: datetime.datetime

class LessonAttemptSchema(Schema):
    id: int
    user: CELUserSchema
    lesson: LessonSchema

class AnswerSchema(Schema):
    question_id: int
    is_correct: int

class QuizAttemptSchema(Schema):
    id: int
    user: CELUserSchema
    quiz: QuizSchema
    answers: List[AnswerSchema]
