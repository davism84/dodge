import datetime
from django.db import models
from django.conf import settings
from django.contrib import admin
from django.utils import timezone

MRN_TYPES = (
	('P', 'EPIC'),
	('M', 'MEDIPAC'),
	('E', 'EMPI'),
)

class LabResult(models.Model):
	record_id = models.IntegerField()
	result_dt = models.DateTimeField('result date')
	result_type = models.CharField(max_length=200)
	result_val =  models.CharField(max_length=200)
	def __str__(self):
		return self.result_type

class Identity(models.Model):
	record_id = models.IntegerField()
	project_id = models.CharField(max_length=200)
	name = models.CharField(max_length=200)	
	def __str__(self):
		return self.name

class Mrn(models.Model):
	mrn = models.CharField(max_length=200)
	mrn_type = models.CharField(max_length=1, choices=MRN_TYPES)
	identity = models.ForeignKey(Identity)
	def __str__(self):
		return self.mrn + ' ' + self.mrn_type

class Project(models.Model):
	project_id = models.CharField(max_length=200)
	user = models.ForeignKey(
    	settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
	def __str__(self):
		return self.project_id + ' ' + self.user.username