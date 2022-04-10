import datetime
from email.policy import default
from statistics import mode
from django.db import models

# Create your models here.
class TestReport(models.Model) :
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone_num = models.IntegerField()
    age = models.IntegerField()
    gender = models.IntegerField()
    height = models.IntegerField()
    weight = models.IntegerField()
    ap_hi = models.IntegerField()
    ap_low = models.IntegerField()
    date = models.DateField(default=datetime.today)