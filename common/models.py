from django.db import models

from common import constants


class Tracker(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class AttemptTracker(models.Model):
    status = models.CharField(max_length=64, choices=constants.STATUSES)
    score = models.IntegerField(default=0)

    started_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    sync_device_id = models.CharField(max_length=255, blank=True, null=True) ## this will be used to determine which device was used to create / update this entry

    class Meta:
        abstract = True


class CommonFields(Tracker):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)

    def __str__(self) -> str:
        return "< {} >".format(self.name)

    class Meta:
        abstract = True

class DescCommonFields(CommonFields):
    description = models.TextField()

    class Meta:
        abstract = True
