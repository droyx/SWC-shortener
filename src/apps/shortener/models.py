from django.db import models
from django.db.models.constraints import UniqueConstraint


class ShortenedURL(models.Model):
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    url: models.URLField = models.URLField(max_length=2000)
    code: models.CharField = models.CharField(max_length=10, db_index=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["code"], name="unique_code"),
            UniqueConstraint(fields=["url"], name="unique_url"),
        ]
