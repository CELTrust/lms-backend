from django.shortcuts import get_object_or_404
from ninja import Router, Schema

from consumer.models import (CELUser, CourseAttempt, LessonAttempt,
                             ProjectUploadAttempt, QuestionAttempt)
from product.models import Course, Lesson

from .schema import (ProjectUploadAttemptSchema, ProjectUploadAttemptSchemaIn,
                     ProjectUploadMarkFinished, SyncCELUserOut, SyncCELUsersIn,
                     SyncCELUsersOut, SyncCourseAttemptOut,
                     SyncCourseAttemptsIn, SyncCourseAttemptsOut,
                     SyncLessonAttemptOut, SyncLessonAttemptsIn,
                     SyncLessonAttemptsOut, SyncQuestionAttemptOut,
                     SyncQuestionAttemptsIn, SyncQuestionAttemptsOut)

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
            user = CELUser.objects.get(gr_number=item.gr_number, school_id=item.school_id)

            course_attempt = CourseAttempt.objects.filter(user=user, course_id=item.course_id).first()
            if course_attempt:
                if course_attempt.can_update(item.updated_at):
                    course_attempt = course_attempt.update_attempt(sync_device_id=item.sync_device_id,
                                                                   score=item.score, updated_at=item.updated_at)
            else:
                course = Course.objects.get(id=item.course_id)
                course_attempt = CourseAttempt.create_attempt(user_id=user.id, course_id=course.id, score=0,
                                                              sync_device_id=item.sync_device_id, updated_at=item.updated_at)

            result = SyncCourseAttemptOut.create_success(course_id=item.course_id, school_id=item.school_id, gr_number=item.gr_number)
            results.append(result)
        except Exception as e:
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
            user = CELUser.objects.get(gr_number=item.gr_number, school_id=item.school_id)

            lesson_attempt = LessonAttempt.objects.filter(user=user, lesson_id=item.lesson_id).first()
            if lesson_attempt:
                if lesson_attempt.can_update(item.updated_at):
                    lesson_attempt = lesson_attempt.update_attempt(sync_device_id=item.sync_device_id, score=item.score,
                                                                   updated_at=item.updated_at)
            else:
                lesson = Lesson.objects.get(id=item.lesson_id)
                lesson_attempt = LessonAttempt.create_attempt(user_id=user.id,lesson_id=lesson.id, score=0, sync_device_id=item.sync_device_id,
                                                              updated_at=item.updated_at)

            result = SyncLessonAttemptOut.create_success(lesson_id=item.lesson_id, school_id=item.school_id, gr_number=item.gr_number)
            results.append(result)
        except Exception as e:
            result = SyncLessonAttemptOut.create_error(lesson_id=item.lesson_id, school_id=item.school_id, gr_number=item.gr_number, detail=e.__str__())
            results.append(result)

    return SyncLessonAttemptsOut(results=results)


@router.post("sync-question-attempts", response=SyncQuestionAttemptsOut)
def sync_question_attempts(request, payload: SyncQuestionAttemptsIn):
    """
    for each item:
        Check if the quiz attempt by the user is already present.
        If yes, ignore it
        if not, create a new one
    """
    results = []
    for item in payload.data:
        try:
            user = CELUser.objects.get(gr_number=item.gr_number, school_id=item.school_id)

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
        except Exception as e:
            result = SyncQuestionAttemptOut.create_error(school_id=item.school_id, question_id=item.question_id,
                                                         gr_number=item.gr_number, detail=e.__str__())
            results.append(result)
    return SyncQuestionAttemptsOut(results=results)


@router.post("sync-cel-users", response=SyncCELUsersOut)
def sync_cel_users(request, payload: SyncCELUsersIn):
    results = []
    for item in payload.data:
        try:
            user = CELUser.objects.filter(gr_number=item.gr_number).first()
            if user and user.school_id != item.school_id:
                    raise Exception("This GR number {0} is already associated with a different school".format(item.gr_number))

            if not user:
                user = CELUser.create(school_id=item.school_id, name=item.name, gr_number=item.gr_number)
            result = SyncCELUserOut.create_success(gr_number=item.gr_number)
            results.append(result)
        except Exception as e:
            result = SyncCELUserOut.create_error(gr_number=item.gr_number, detail=e.__str__())
            results.append(result)
    return SyncCELUsersOut(results=results)

@router.post("get-upload-details", response=ProjectUploadAttemptSchema)
def get_upload_details(request, payload: ProjectUploadAttemptSchemaIn):
    user = get_object_or_404(CELUser, gr_number=payload.gr_number, school_id=payload.school_id)
    course = get_object_or_404(Course, id=payload.course_id)
    return ProjectUploadAttempt.create_new(user_id=user.id, course_id=course.id, file=payload.filename,
                                           updated_at=payload.updated_at)

@router.post("mark-upload-finished", response=ProjectUploadAttemptSchema)
def mark_upload_finished(request, payload: ProjectUploadMarkFinished):
    return ProjectUploadAttempt.mark_finished(payload.id)
