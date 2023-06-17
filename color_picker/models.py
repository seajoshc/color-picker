from django.db import models


class Color(models.Model):
    question_text = models.CharField(max_length=25)
    modified_date = models.DateTimeField("last modified date")
