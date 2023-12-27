import datetime
from ast import Mod
from dataclasses import field
from optparse import Option
from typing import List

from ninja import ModelSchema, Schema

from product.models import Course, Lesson, Question, School


class CourseSchema(ModelSchema):
    class Meta:
        model = Course
        fields = '__all__'


class SchoolSchema(ModelSchema):
    class Meta:
        model = School
        fields = '__all__'


class LessonSchema(ModelSchema):
    class Meta:
        model = Lesson
        fields = '__all__'

class OptionSchema(Schema):
    id: int
    text: str
    is_correct: bool

class QuestionSchema(Schema):
    id: int
    lesson_id: int
    text: str
    options: List[OptionSchema]
