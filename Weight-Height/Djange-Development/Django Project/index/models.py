from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class StudentModel(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    Gender=models.CharField(max_length=10)
    Height=models.FloatField()
    Weight=models.FloatField()