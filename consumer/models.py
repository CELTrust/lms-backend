from django.db import models
from common.models import CommonFields, Tracker, AttemptTracker
from product.models import Question, Quiz, Lesson, Course

# Create your models here.

# Consumer
class School(CommonFields):
    pass

class CELUser(Tracker):
    name = models.CharField(max_length=255)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    rollnum = models.CharField(max_length=255)

    class Meta:
        unique_together = (("school", "rollnum"),)

    def __str__(self) -> str:
        return "< {} >".format(self.name)

class Answer(Tracker):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="answers")
    user = models.ForeignKey(CELUser, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    is_correct = models.BooleanField()

class CourseAttempt(AttemptTracker, Tracker):
    user = models.ForeignKey(CELUser, on_delete=models.CASCADE, related_name="course_attempts")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="attempts")

class LessonAttempt(AttemptTracker, Tracker):
    course_attempt = models.ForeignKey(CourseAttempt, on_delete=models.CASCADE, related_name="course_attempts")
    user = models.ForeignKey(CELUser, on_delete=models.CASCADE, related_name="lesson_attempts")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="attempts")
    project_upload_link = models.FileField(blank=True, null=True)


class QuizAttempt(AttemptTracker, Tracker):
    lesson_attempt = models.ForeignKey(LessonAttempt, on_delete=models.CASCADE, related_name="quiz_attempts")
    user = models.ForeignKey(CELUser, on_delete=models.CASCADE, related_name="quiz_attempts")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="attempts")
    score = models.IntegerField(default=0)
