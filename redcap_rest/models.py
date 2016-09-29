import datetime
from django.db import models
from django.utils import timezone

class LabResult(models.Model):
	record_id = models.IntegerField()
	result_dt = models.DateTimeField('result date')
	result_type = models.CharField(max_length=200)
	result_val =  models.CharField(max_length=200)
	def __str__(self):
		return self.result_type