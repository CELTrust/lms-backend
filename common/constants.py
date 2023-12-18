from enum import Enum

STATUS_STARTED = "started"
STATUS_FINISHED = "finished"

STATUSES = (
    (STATUS_STARTED, STATUS_STARTED),
    (STATUS_FINISHED, STATUS_FINISHED)
)

class StatusChoices(Enum):
    finished: STATUS_FINISHED
    started: STATUS_STARTED

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
