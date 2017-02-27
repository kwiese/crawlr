from django.db import models

class Feedback(models.Model):
    fb_neg = models.CharField(max_length=50)
    fb_pos = models.CharField(max_length=50)
    fb_date = models.DateField()
