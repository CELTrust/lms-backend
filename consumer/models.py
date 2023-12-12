from django.db import models
from common.models import Tracker, AttemptTracker
from product.models import Option, Question, Quiz, Lesson, Course, School

class CELUser(Tracker):
    name = models.CharField(max_length=255)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    gr_num = models.CharField(max_length=255)

    class Meta:
        unique_together = (("school", "gr_num"),)

    def __str__(self) -> str:
        return "< {} >".format(self.name)


class CourseAttempt(AttemptTracker, Tracker):
    user = models.ForeignKey(CELUser, on_delete=models.CASCADE, related_name="course_attempts")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="attempts")

    class Meta:
        unique_together = (("user", "course"),)

class LessonAttempt(AttemptTracker, Tracker):
    user = models.ForeignKey(CELUser, on_delete=models.CASCADE, related_name="lesson_attempts")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="attempts")

    class Meta:
        unique_together = (("user", "lesson"),)


class ProjectUploadAttempt(Tracker):
    user = models.ForeignKey(CELUser, on_delete=models.CASCADE, related_name="project_upload_attempts")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="project_upload_attempts")

    file = models.FileField()
    size = models.IntegerField()

    class Meta:
        unique_together = (("user", "course"))


class QuizAttempt(AttemptTracker, Tracker):
    user = models.ForeignKey(CELUser, on_delete=models.CASCADE, related_name="quiz_attempts")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="attempts")


# TODO: maybe this can be removed in the first iteration?
class QuestionAttempt(Tracker):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="answers")
    user = models.ForeignKey(CELUser, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    options = models.ManyToManyField(Option)
    is_correct = models.BooleanField()
