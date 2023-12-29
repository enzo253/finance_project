# finance_app/models.py
from django.db import models

class Transaction(models.Model):
    date = models.DateField()
    amount = models.FloatField()
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    net_profit = models.CharField(max_length=10)
