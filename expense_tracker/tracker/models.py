# from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    category = models.CharField(max_length=50)
    date = models.DateField()
    type = models.CharField(max_length=10)
    note = models.TextField(blank=True)
