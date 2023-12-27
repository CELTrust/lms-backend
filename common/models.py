import random

from django.db import models
from django.utils.text import slugify

from common import constants


class Tracker(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class AttemptTracker(models.Model):
    status = models.CharField(max_length=64, choices=constants.STATUSES, default=constants.STATUS_STARTED)
    score = models.IntegerField(default=0)
    sync_device_id = models.CharField(max_length=255)

    started_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def can_update(self, updated_at) -> bool:
        return not self.has_finished() and updated_at > self.updated_at

    def has_finished(self) -> bool:
        return self.status == constants.STATUS_FINISHED

    @classmethod
    def exists(cls, id) -> bool:
        return cls.objects.filter(id=id).exists()


    class Meta:
        abstract = True


class CommonFields(Tracker):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)

    def __str__(self) -> str:
        return "{}".format(self.slug)

    class Meta:
        abstract = True

    def randomify(self, slug):
        return "{0}-{1}".format(slug, random.randint(1, 1000))

    def generate_unique_slug(self, slug):
        if self.__class__.objects.filter(slug=slug).exists():
            new_slug = self.randomify(slug=slug)
            return self.generate_unique_slug(new_slug)
        return slug

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = self.generate_unique_slug(slugify(self.name))
        return super().save(*args, **kwargs)


class DescCommonFields(CommonFields):
    description = models.TextField()

    class Meta:
        abstract = True
