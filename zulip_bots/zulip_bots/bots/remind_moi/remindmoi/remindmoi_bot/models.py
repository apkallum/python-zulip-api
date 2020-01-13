import pytz

from datetime import datetime

from django.db import models


class Reminder(models.Model):
    reminder_id = models.AutoField(primary_key=True)

    zulip_user_id = models.PositiveIntegerField()
    title = models.CharField(max_length=150)
    created = models.DateTimeField()
    deadline = models.DateTimeField()
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Convert incoming unix ts to datetime objects before saving
        self.created = datetime.utcfromtimestamp(self.created).replace(tzinfo=pytz.utc)
        self.deadline = datetime.utcfromtimestamp(self.deadline).replace(tzinfo=pytz.utc)
        super().save(*args, **kwargs)


"""
    {
        "zulip_user_id": 100,
        "title": "asdhjklasdf",
        "created": 1578941197,
        "deadline": 1580755597.0,
        "active": "True"
    }
"""
