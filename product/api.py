from ninja import Router
from .models import Course, Lesson, Quiz
from .schema import CourseSchema, LessonSchema, QuizSchema
from typing import List

router = Router()


@router.get("courses", response=List[CourseSchema])
def list_courses(request):
    courses = Course.objects.all()
    return courses

@router.get("lessons", response=List[LessonSchema])
def list_lessons(request):
    lessons = Lesson.objects.all()
    return lessons

@router.get("quizzes", response=List[QuizSchema])
def get_quiz(request):
    quizes = Quiz.objects.all()
    return quizes
