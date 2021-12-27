from django.db import models


class Widget(models.Model):
    url = models.URLField(blank=True)

