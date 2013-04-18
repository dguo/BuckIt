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
	count = models.IntegerField(default=1)
	def __unicode__(self):
		return self.task_text

class User(models.Model):
	name = models.CharField(max_length=40)
	password = models.CharField(max_length=40)
	friends = models.ManyToManyField("self", null=True, blank=True)
	tasks = models.ManyToManyField(Task, through="Ownership")
	def __unicode__(self):
		return self.name

class Ownership(models.Model):
	user = models.ForeignKey(User)
	task = models.ForeignKey(Task)
	completed = models.BooleanField(default=False)
	date_set = models.DateTimeField(auto_now_add=True)
	date_done = models.DateTimeField(null=True, blank=True)
	def __unicode__(self):
		return self.user.name + " : " + self.task.task_text