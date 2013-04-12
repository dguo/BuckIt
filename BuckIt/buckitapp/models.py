from django.db import models
import datetime
from django.utils import timezone


class Tag(models.Model):
	tag_text = models.CharField(max_length=40)
	def __unicode__(self):
		return self.tag_text

class Task(models.Model):
	task_text = models.CharField(max_length=140)
	tags = models.ManyToManyField(Tag)
	def __unicode__(self):
		return self.task_text

class User(models.Model):
	name = models.CharField(max_length=40)
	#friends = models.ManyToManyField(User)
	#tasks = models.ManyToManyField(Task, through="Ownership")
	tasks = models.ManyToManyField(Task)
	def __unicode__(self):
		return self.name

class Ownership(models.Model):
	user = models.ForeignKey(User)
	task = models.ForeignKey(Task)
	completed = models.BooleanField(default=False)
	start_time = models.DateTimeField()
	complete_time = models.DateTimeField()