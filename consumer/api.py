from django.http import Http404
from django.shortcuts import get_object_or_404
from ninja import Router

from common import constants
from consumer.models import (CELUser, CourseAttempt, LessonAttempt,
                             QuestionAttempt, QuizAttempt)
from product.models import Course, Lesson

from .schema import (SyncCourseAttemptOut, SyncCourseAttemptsIn,
                     SyncCourseAttemptsOut, SyncLessonAttemptOut,
                     SyncLessonAttemptsIn, SyncLessonAttemptsOut,
                     SyncQuizAttemptOut, SyncQuizAttemptSchema,
                     SyncQuizAttemptsOut)

router = Router(tags=["Consumer"])


@router.post("sync-course-attempts", response=SyncCourseAttemptsOut)
def sync_course_attempts(request, payload: SyncCourseAttemptsIn):
    """
    for each item in the payload
        If course attempt is present and is not updated, update it
        else create a new course attempt
    """
    results = []
    for item in payload.data:
        try:
            user = get_object_or_404(
                CELUser, gr_number=item.gr_number, school_id=item.school_id
            )

            course_attempt = CourseAttempt.objects.filter(
                user=user, course_id=item.course_id
            ).first()
            if course_attempt:
                if course_attempt.can_update(item.updated_at):
                    course_attempt = course_attempt.update_attempt(
                        sync_device_id=item.sync_device_id,
                        score=item.score,
                        updated_at=item.updated_at,
                    )
            else:
                course = get_object_or_404(Course, id=item.course_id)
                course_attempt = CourseAttempt.create_attempt(
                    user_id=user.id,
                    course_id=course.id,
                    score=0,
                    sync_device_id=item.sync_device_id,
                    updated_at=item.updated_at,
                )

            result = SyncCourseAttemptOut.create_success(
                course_id=item.course_id,
                school_id=item.school_id,
                gr_number=item.gr_number,
            )
            results.append(result)
        except Http404 as e:
            result = SyncCourseAttemptOut.create_error(
                course_id=item.course_id,
                school_id=item.school_id,
                gr_number=item.gr_number,
                detail=e.__str__(),
            )
            results.append(result)

    return SyncCourseAttemptsOut(results=results)


@router.post("sync-lesson-attempts", response=SyncLessonAttemptsOut)
def create_lesson_attempt(request, payload: SyncLessonAttemptsIn):
    """
    for each item:
        If lesson attempt is present and is not updated, update it
        else create a new lesson attempt
    """
    results = []
    for item in payload.data:
        try:
            user = get_object_or_404(
                CELUser, gr_number=item.gr_number, school_id=item.school_id
            )

            lesson_attempt = LessonAttempt.objects.filter(
                user=user, lesson_id=item.lesson_id
            ).first()
            if lesson_attempt:
                if lesson_attempt.can_update(item.updated_at):
                    lesson_attempt = lesson_attempt.update_attempt(
                        sync_device_id=item.sync_device_id,
                        score=item.score,
                        updated_at=item.updated_at,
                    )
            else:
                lesson = get_object_or_404(Lesson, id=item.lesson_id)
                lesson_attempt = LessonAttempt.create_attempt(
                    user_id=user.id,
                    lesson_id=lesson.id,
                    score=0,
                    sync_device_id=item.sync_device_id,
                    updated_at=item.updated_at,
                )

            result = SyncLessonAttemptOut.create_success(
                lesson_id=item.lesson_id,
                school_id=item.school_id,
                gr_number=item.gr_number,
            )
            results.append(result)
        except Http404 as e:
            result = SyncLessonAttemptOut.create_error(
                lesson_id=item.lesson_id,
                school_id=item.school_id,
                gr_number=item.gr_number,
                detail=e.__str__(),
            )
            results.append(result)

    return SyncLessonAttemptsOut(results=results)


@router.post("sync-quiz-attempts", response=SyncQuizAttemptsOut)
def create_quiz_attempt(request, payload: SyncQuizAttemptSchema):
    """
    for each item:
        Check if the quiz attempt by the user is already present.
        If yes, ignore it
        if not, create a new one
    """
    results = []
    for item in payload.data:
        try:
            user = get_object_or_404(
                CELUser, gr_number=item.gr_number, school_id=item.school_id
            )

            quiz_attempt = QuizAttempt.objects.filter(
                user=user, quiz_id=item.quiz_id
            ).first()
            if quiz_attempt:
                if quiz_attempt.can_update(item.updated_at):
                    quiz_attempt.sync_device_id = item.sync_device_id
                    quiz_attempt.updated_at = item.updated_at

                    quiz_attempt.answers.all().delete()
                    score = 0
                    for qa in item.question_attempts:
                        if qa.is_correct:
                            score += 1
                        QuestionAttempt.objects.create(
                            question_id=qa.question_id,
                            quiz_id=item.quiz_id,
                            user=user,
                            is_correct=qa.is_correct,
                            updated_at=item.updated_at,
                        )

                    quiz_attempt.score = score
                    quiz_attempt.save()
            else:
                quiz_attempt = QuizAttempt.objects.create(
                    user=user,
                    quiz_id=item.quiz_id,
                    status=constants.STATUS_FINISHED,
                    sync_device_id=item.sync_device_id,
                    created_at=item.updated_at,
                    updated_at=item.updated_at,
                )

                score = 0
                for qa in item.question_attempts:
                    if qa.is_correct:
                        score += 1
                    QuestionAttempt.objects.create(
                        question_id=qa.question_id,
                        quiz_id=item.quiz_id,
                        user=user,
                        is_correct=qa.is_correct,
                        updated_at=item.updated_at,
                    )

                quiz_attempt.score = score
                quiz_attempt.save()

            result = SyncQuizAttemptOut.create_success(school_id=item.school_id, quiz_id=item.quiz_id, gr_number=item.gr_number)
            results.append(result)
        except Http404 as e:
            result = SyncCourseAttemptOut.create_error(school_id=item.school_id, quiz_id=item.quiz_id, gr_number=item.gr_number)
            results.append(result)
    return SyncQuizAttemptsOut(results=results)
