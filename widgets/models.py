from django.db import models


class Widget(models.Model):
    url = models.URLField(max_length=255, null=True, blank=True)

