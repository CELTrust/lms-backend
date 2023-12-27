from django.http import Http404
from django.shortcuts import get_object_or_404
from ninja import Router, Schema

from consumer.models import (CELUser, CourseAttempt, LessonAttempt,
                             QuestionAttempt)
from product.models import Course, Lesson

from .schema import (SyncCELUsersIn, SyncCELUsersOut, SyncCourseAttemptOut,
                     SyncCourseAttemptsIn, SyncCourseAttemptsOut,
                     SyncLessonAttemptOut, SyncLessonAttemptsIn,
                     SyncLessonAttemptsOut, SyncQuestionAttemptOut,
                     SyncQuestionAttemptsIn, SyncQuestionAttemptsOut)

router = Router(tags=["Consumer"])

class Response(Schema):
    message: str


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
            user = get_object_or_404(CELUser, gr_number=item.gr_number, school_id=item.school_id)

            course_attempt = CourseAttempt.objects.filter(user=user, course_id=item.course_id).first()
            if course_attempt:
                if course_attempt.can_update(item.updated_at):
                    course_attempt = course_attempt.update_attempt(sync_device_id=item.sync_device_id,
                                                                   score=item.score, updated_at=item.updated_at)
            else:
                course = get_object_or_404(Course, id=item.course_id)
                course_attempt = CourseAttempt.create_attempt(user_id=user.id, course_id=course.id, score=0,
                                                              sync_device_id=item.sync_device_id, updated_at=item.updated_at)

            result = SyncCourseAttemptOut.create_success(course_id=item.course_id, school_id=item.school_id, gr_number=item.gr_number)
            results.append(result)
        except Http404 as e:
            result = SyncCourseAttemptOut.create_error(course_id=item.course_id, school_id=item.school_id, gr_number=item.gr_number,
                                                       detail=e.__str__())
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

            lesson_attempt = LessonAttempt.objects.filter(user=user, lesson_id=item.lesson_id).first()
            if lesson_attempt:
                if lesson_attempt.can_update(item.updated_at):
                    lesson_attempt = lesson_attempt.update_attempt(sync_device_id=item.sync_device_id, score=item.score,
                                                                   updated_at=item.updated_at)
            else:
                lesson = get_object_or_404(Lesson, id=item.lesson_id)
                lesson_attempt = LessonAttempt.create_attempt(user_id=user.id,lesson_id=lesson.id, score=0, sync_device_id=item.sync_device_id,
                                                              updated_at=item.updated_at)

            result = SyncLessonAttemptOut.create_success(lesson_id=item.lesson_id, school_id=item.school_id, gr_number=item.gr_number)
            results.append(result)
        except Http404 as e:
            result = SyncLessonAttemptOut.create_error(lesson_id=item.lesson_id, school_id=item.school_id, gr_number=item.gr_number, detail=e.__str__())
            results.append(result)

    return SyncLessonAttemptsOut(results=results)


@router.post("sync-question-attempts", response=SyncQuestionAttemptsOut)
def create_quiz_attempt(request, payload: SyncQuestionAttemptsIn):
    """
    for each item:
        Check if the quiz attempt by the user is already present.
        If yes, ignore it
        if not, create a new one
    """
    results = []
    for item in payload.data:
        try:
            user = get_object_or_404(CELUser, gr_number=item.gr_number, school_id=item.school_id)

            score = 0
            if item.is_correct:
                score = 1

            question_attempt = QuestionAttempt.objects.filter(
                user=user, question_id=item.question_id
            ).first()
            if question_attempt:
                if question_attempt.can_update(item.updated_at):

                    question_attempt.update_attempt(score=score, sync_device_id=item.sync_device_id, updated_at=item.updated_at)
            else:

                question_attempt = QuestionAttempt.create_attempt(user_id=user.id, question_id=item.question_id,
                                                                  score=score, sync_device_id=item.sync_device_id, updated_at=item.updated_at)

            result = SyncQuestionAttemptOut.create_success(school_id=item.school_id, question_id=item.question_id, gr_number=item.gr_number)
            results.append(result)
        except Http404 as e:
            result = SyncQuestionAttemptOut.create_error(school_id=item.school_id, question_id=item.question_id,
                                                         gr_number=item.gr_number, detail=e.__str__())
            results.append(result)
    return SyncQuestionAttemptsOut(results=results)


@router.post("sync-cel-users", response=SyncCELUsersOut)
def sync_cel_users(request, payload: SyncCELUsersIn):
    pass
