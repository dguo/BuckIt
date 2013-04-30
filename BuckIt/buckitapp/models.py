from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User


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

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	name = models.CharField(max_length=40)
	friends = models.ManyToManyField("self", null=True, blank=True)
	tasks = models.ManyToManyField(Task, through="Ownership")
	def __unicode__(self):
		return self.name

class Ownership(models.Model):
	userProfile = models.ForeignKey(UserProfile)
	task = models.ForeignKey(Task)
	completed = models.BooleanField(default=False)
	date_set = models.DateTimeField(auto_now_add=True)
	date_done = models.DateTimeField(null=True, blank=True)
	def __unicode__(self):
		return self.userProfile.name + " : " + self.task.task_text