import datetime
from typing import List

from ninja import ModelSchema, Schema

from product.models import Course


class CourseSchema(ModelSchema):
    class Meta:
        model = Course
        fields = '__all__'

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
    lesson_id: int
    text: str
    options: List[OptionSchema]

class SchoolSchema(Schema):
    id: int
    name: str
    slug: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
