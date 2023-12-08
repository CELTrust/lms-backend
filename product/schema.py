from typing import List
from ninja import Schema
import datetime

class CourseSchema(Schema):
    id: int
    name: str
    slug: str
    description: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

class LessonSchema(Schema):
    id: int
    name: str
    slug: str
    description: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    video_link: str
    presentation_link: str
    course_id: int
    has_project: bool

class OptionSchema(Schema):
    id: int
    text: str
    is_correct: bool

class QuestionSchema(Schema):
    id: int
    text: str
    options: List[OptionSchema]

class QuizSchema(Schema):
    id: int
    lesson_id: int
    questions: List[QuestionSchema]

class SchoolSchema(Schema):
    id: int
    name: str
    slug: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

class AllSchema(Schema):
    schools: List[SchoolSchema]
    courses: List[CourseSchema]
    lessons: List[LessonSchema]
    quizzes: List[QuizSchema]
