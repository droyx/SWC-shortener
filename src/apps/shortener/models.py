from django.db import models
from django.db.models.constraints import UniqueConstraint


class ShortenedURL(models.Model):
    url = models.URLField(max_length=2000)
    code = models.CharField(max_length=10, db_index=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["code"], name="unique_code"),
            UniqueConstraint(fields=["url"], name="unique_url"),
        ]
