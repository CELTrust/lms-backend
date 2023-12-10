from ninja import Router
from .models import Course, Lesson, Quiz
from .schema import AllSchema, CourseSchema, LessonSchema, QuizSchema
from typing import List

router = Router()


@router.get("courses", response=List[CourseSchema])
def list_courses(request):
    courses = Course.objects.all()
    return courses

@router.get("{course_id}/lessons", response=List[LessonSchema])
def list_lessons(request, course_id: int):
    lessons = Lesson.objects.filter(course_id=course_id)
    return lessons

@router.get("{lesson_id}/quiz", response=QuizSchema)
def get_quiz(request, lesson_id: int):
    quiz = Quiz.objects.filter(lesson_id=lesson_id).first()
    return quiz


# @router.get("get-all", response=AllSchema)
# def list_all(request):
#     courses = Course.objects.all()
#     lessons = Lesson.objects.all()
#     quiz = Quiz.objects.all().prefetch_related('questions')

#     response = AllSchema(courses=[], lessons=[], quiz=None)
#     return response