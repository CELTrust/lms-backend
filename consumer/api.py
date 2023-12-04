from ast import List
import datetime
from django.shortcuts import get_object_or_404
from ninja import Field, Router, Schema
from common import constants
from common.models import AttemptTracker
from consumer.models import Answer, CELUser, CourseAttempt, LessonAttempt, QuizAttempt
from .schema import CourseAttemptSchema, CreateCourseAttemptIn, CreateLessonAttemptIn, LessonAttemptSchema, QuizAttemptSchema, CreateQuizAttemptIn
from product.schema import CourseSchema, LessonSchema, QuizSchema

router = Router()

@router.post("course-attempts", response=CourseAttemptSchema)
def create_course_attempt(request, payload: CreateCourseAttemptIn):
    course_attempt = CourseAttempt.objects.create(
        user_id=payload.user_id, course_id=payload.course_id,
        started_at=datetime.datetime.now(), status=constants.STATUS_STARTED
    )
    return course_attempt

@router.post("lesson-attempts", response=LessonAttemptSchema)
def create_lesson_attempt(request, payload: CreateLessonAttemptIn):
    lesson_attempt = LessonAttempt.objects.create(
        user_id=payload.user_id, lesson_id=payload.lesson_id,
        started_at=datetime.datetime.now(), status=constants.STATUS_STARTED
    )
    return lesson_attempt

@router.post("quiz-attempts", response=QuizAttemptSchema)
def create_quiz_attempt(request, paylaod: CreateQuizAttemptIn):
    quiz_attempt = QuizAttempt.objects.create(
        user_id=paylaod.user_id, quiz_id=paylaod.quiz_id,
        started_at=datetime.datetime.now(), status=constants.STATUS_STARTED
    )
    return quiz_attempt

@router.put("quiz-attempts/{attempt_id}", response=QuizAttemptSchema)
def update_quiz_attempt(request, attempt_id: int, payload: UpdateQuizAttemptIn):
    quiz_attempt = get_object_or_404(QuizAttempt, id=attempt_id)
    for answer in payload.answers:
        Answer.objects.create(quiz=quiz_attempt.quiz, user=payload.user_id, question_id=answer.question_id, is_correct=answer.is_correct)

    if quiz_attempt.is_complete():
        quiz_attempt.mark_finished()

        lesson_attempt = quiz_attempt.lesson_attempt
        if lesson_attempt.is_complete():
            lesson_attempt.mark_finished()

            course_attempt = lesson_attempt.course_attempt
            if course_attempt.is_complete():
                course_attempt.mark_finished()

    return quiz_attempt

@router.get("/course-attempts", response=List[CourseAttemptSchema])
def list_user_course_attempts(request, course_id: int):
    user_id = 1 # replace this with getting user from session
    course_attempts = CourseAttempt.objects.filter(user_id=user_id)
    return course_attempts

@router.get("course-attempts/{course_id}", response=CourseAttemptSchema)
def get_recent_course_attempt(request, course_id: int):
    course_attempt = CourseAttempt.objects.filter(user_id=1, course_id=course_id).last()
    return course_attempt

@router.get("lesson-attempts/{lesson_id}", response=LessonAttemptSchema)
def list_lesson_attempts(request, lesson_id: int):
    lesson_attempt = LessonAttempt.objects.filter(user_id=1, lesson_id=lesson_id).last()
    return lesson_attempt

@router.get("quiz-attempts/{quiz_id}", response=QuizAttemptSchema)
def list_quiz_attempts(request, quiz_id: int):
    quiz_attempt_schema = QuizAttempt.objects.filter(user_id=1, quiz_id=quiz_id).last()
    return quiz_attempt_schema
