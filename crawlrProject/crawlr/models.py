from django.db import models
from django.contrib.auth.models import User
#from oauth2client.contrib.django_orm import FlowField
from oauth2client.contrib.django_util.models import CredentialsField
from django.contrib.auth.models import User

class Feedback(models.Model):
    fb_neg = models.CharField(max_length=50)
    fb_pos = models.CharField(max_length=50)
    fb_date = models.DateField()

class CredentialsModel(models.Model):
    user_id = models.OneToOneField(User)
    credential = CredentialsField()
