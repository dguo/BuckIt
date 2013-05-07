from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User

class Badge(models.Model):
	badge_title = models.CharField(max_length=50)
	badge_text = models.CharField(max_length=50)
	bad_pic = models.CharField(max_length=300)
	def __unicode__(self):
		return self.badge_title

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
	fb_id = models.CharField(max_length=300, null=True, default=3)
	fb_pic = models.CharField(max_length=300, null=True)
	friends = models.ManyToManyField("self", null=True, blank=True)
	tasks = models.ManyToManyField(Task, through="Ownership")
	badges = models.ManyToManyField(Badge)
	def __unicode__(self):
		return self.name

class Ownership(models.Model):
	userProfile = models.ForeignKey(UserProfile, null=True)
	task = models.ForeignKey(Task, null=True)
	completed = models.BooleanField(default=False)
	date_set = models.DateTimeField(auto_now_add=True)
	date_done = models.DateTimeField(null=True, blank=True)
	def __unicode__(self):
		return self.userProfile.name + " : " + self.task.task_text