from typing import List

from ninja import Router
from ninja.pagination import paginate

from .models import Course, Lesson, Question, School
from .schema import CourseSchema, LessonSchema, QuestionSchema, SchoolSchema

router = Router(tags=["Product"])

@router.get("schools", response=List[SchoolSchema])
@paginate
def list_schools(request):
    schools = School.objects.all()
    return schools

@router.get("courses", response=List[CourseSchema])
@paginate
def list_courses(request):
    courses = Course.objects.all()
    return courses

@router.get("lessons", response=List[LessonSchema])
@paginate
def list_lessons(request):
    lessons = Lesson.objects.all()
    return lessons

@router.get("questions", response=List[QuestionSchema])
@paginate
def get_questions(request):
    quizes = Question.objects.all()
    return quizes
