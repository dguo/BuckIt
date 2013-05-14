# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from models import Badge, Tag, Task, UserProfile, Ownership
from django.contrib.auth import authenticate 
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import itertools, operator, json, urllib2
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib import messages

def home(request):
	storage = messages.get_messages(request)
	storage.used = True

	loggedin = False

	if request.user.is_authenticated():

		loggedin = True
		
		userProfile_obj = get_object_or_404(UserProfile, user=request.user)

		username = userProfile_obj.name

		if request.method == 'POST':
			
			if 'addTask' in request.POST:
			    # create the new tag task if it doesn't exist already
			    tag_sub = request.POST['hidden-tags'].lower().split(',')
			    tagbox_sub = request.POST['tags'].lower().split(',')
			    
			    alltags = itertools.chain(tag_sub,tagbox_sub)

			    tag_list = set()

			    for tag in alltags:

			    	if tag != "":
			    		new_tag = Tag.objects.filter(tag_text=tag)

			    		if len(new_tag) == 1:
			    			new_tag = new_tag[0]
			    			tag_list.add(new_tag)
			    		else:
			    			new_tag = Tag(tag_text=tag)
			    			tag_list.add(new_tag)
			    			new_tag.save()

			    # create the new task if it doesn't exist already
			    new_task = Task.objects.filter(task_text=request.POST['task'])
			    if len(new_task) == 1:
			    	pass
			    else:
			    	new_task = Task(task_text=request.POST['task'])
			    	new_task.save()
			    	for tag in tag_list:
			    		new_task.tags.add(tag)
			    	new_ownership = Ownership(userProfile=userProfile_obj, task=new_task)
			    	new_ownership.save()

			    return HttpResponseRedirect('')

			elif 'recInfo' in request.POST:
				taskTxt = request.POST['recInfo']
				addedtask = get_object_or_404(Task, task_text=taskTxt)
				addedtask.count = addedtask.count + 1
				addedtask.save()
				new_ownership = Ownership(userProfile=userProfile_obj, task=addedtask)
				new_ownership.save()

				return HttpResponseRedirect('')

			elif 'checkInfo' in request.POST:
				taskTxt = request.POST['checkInfo']
				checkedtask = get_object_or_404(Task, task_text=taskTxt)
				checkedOwn = get_object_or_404(Ownership, task=checkedtask, userProfile=userProfile_obj)
				if checkedOwn.completed is False:
					checkedOwn.completed = True
					checkedOwn.date_done = datetime.now()
					badge_count = userProfile_obj.badges.count()
					check_badges(request, groupie=False)
					if (userProfile_obj.badges.count() > badge_count):
						messages.info(request, "1")
				else:
					checkedOwn.completed = False
				checkedOwn.save()

				return HttpResponseRedirect(request.path)

			elif 'trashInfo' in request.POST:
				taskTxt = request.POST['trashInfo']
				checkedtask = get_object_or_404(Task, task_text=taskTxt)
				checkedOwn = get_object_or_404(Ownership, task=checkedtask, userProfile=userProfile_obj)
				checkedOwn.delete()

				return HttpResponseRedirect('')

			elif 'delete_account' in request.POST:
				currentUser = request.user
				currentUser.is_active = False
				currentUser.save()
				logout(request)
				return HttpResponseRedirect('/login/')


		else:

			try:

				social_auth = request.user.social_auth.get(provider='facebook')
				userProfile_obj.fb_id = social_auth.uid
				userProfile_obj.fb_pic = "http://graph.facebook.com/" + social_auth.uid + "/picture"
				userProfile_obj.save()

				friendsurl = "https://graph.facebook.com/" + social_auth.uid + "/friends?access_token=" + social_auth.extra_data['access_token']
				friendJson = urllib2.urlopen(friendsurl)
				friendJS = json.load(friendJson)
				friendDict = friendJS['data']

				for friend in friendDict:
					try:
						fb_id = friend['id'].encode('utf-8')
						f = UserProfile.get(fb_id=fb_id)
						userProfile_obj.friends.add(f)
					except:
						pass
			except:
				pass

			owns1 = Ownership.objects.filter(userProfile=userProfile_obj).filter(completed=False).order_by('-date_set')
			owns2 = Ownership.objects.filter(userProfile=userProfile_obj).filter(completed=True).order_by('-date_done')
			owns = itertools.chain(owns1, owns2)
			ownTasks = Ownership.objects.filter(userProfile=userProfile_obj).values('task')
			topTasks = Task.objects.order_by('-count').exclude(id__in=ownTasks)[0:3]
			
			setNews = Ownership.objects.none()
			doneNews = Ownership.objects.none()
			for f in userProfile_obj.friends.all():
				fset = Ownership.objects.filter(userProfile=f).filter(completed=False)[0:5]
				fdone = Ownership.objects.filter(userProfile=f).filter(completed=True)[0:5]
				setNews = itertools.chain(setNews, fset)
				doneNews = itertools.chain(doneNews, fdone)
			
			setList = list(setNews)
			setList = sorted(setList, key=operator.attrgetter('date_set'), reverse=True)

			doneList = list(doneNews)
			doneList = sorted(doneList, key=operator.attrgetter('date_done'), reverse=True)

			setIndex = 0
			doneIndex = 0
			friendNews = []
			for i in range(5):
				if (doneIndex >= len(doneList)):
					if (setIndex >= len(setList)):
						break
					else:
						friendNews.append(setList[setIndex])
						setIndex = setIndex + 1
				else:
					if (setIndex >= len(setList)):
						friendNews.append(doneList[doneIndex])
						doneIndex = doneIndex + 1
					else:
						if (setList[setIndex].date_set > doneList[doneIndex].date_done):
							friendNews.append(setList[setIndex])
							setIndex = setIndex + 1
						else:
							friendNews.append(doneList[doneIndex])
							doneIndex = doneIndex + 1

			for i in friendNews:
				print i.task.task_text
			return render_to_response('home.html',
			                          {'topTasks':topTasks, 'owns':owns, 'loggedin':loggedin,
			                          'name':username, 'userpic':userProfile_obj.fb_pic, 'friendNews':friendNews},
			                          context_instance=RequestContext(request))	
	
	# user is not logged in
	else:
		return HttpResponseRedirect('/login/')

def login(request, errorcode=None):
	logout(request)
	storage = messages.get_messages(request)
	storage.used = True
	if request.method == 'POST':

		# login the user; return an error message if applicable
		if 'login' in request.POST:
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					auth_login(request, user)
					if request.user.is_authenticated():
						return HttpResponseRedirect('/home')
				else:
					# Return a 'disabled account' error message
					return HttpResponseRedirect('/login/1/')
			else:
				# return an 'invalid login' error message
				return HttpResponseRedirect('/login/1/')

		# make a new account
		if 'create' in request.POST:
			username = request.POST['username']

			try:
				User.objects.get(username=username)
				return HttpResponseRedirect('/login/2/')
			except:
				first_name = request.POST['firstname']
				last_name = request.POST['lastname']
				password = request.POST['password']
				name = first_name + ' ' + last_name
				new_user = User.objects.create_user(username, '', password)
				new_user.save()
				new_user_profile = UserProfile(user=new_user, name=name)
				new_user_profile.save()
				user = authenticate(username=username, password=password)
				auth_login(request, user)
				return HttpResponseRedirect('/home')
	else:
		if errorcode == "1":
			loginerror = "Incorrect username or password."
			registererror = ""
		elif errorcode =="2":
			loginerror = ""
			registererror = "Username already taken. Please choose another one."
		else:
			loginerror = ""
			registererror = ""
			error = ""

		return render_to_response('login.html', {'loginerror':loginerror, 'registererror':registererror, 'errorcode':errorcode}, context_instance=RequestContext(request))

def profile(request, userid):
	storage = messages.get_messages(request)
	storage.used = True

	newid = userid.replace('_',' ')

	profIsUser = False
	if request.user.is_authenticated():
		loggedin = True
		userProfile_obj = get_object_or_404(UserProfile, user=request.user)
		name = userProfile_obj.name
		profUser = get_object_or_404(UserProfile, name=newid)
		profPic = profUser.fb_pic
		badges = profUser.badges.all()
		owntasks = userProfile_obj.tasks.all()

		if request.method == 'POST':
			taskTxt = request.POST['addtaskbutton']
			addedtask = get_object_or_404(Task, task_text=taskTxt)
			addedtask.count = addedtask.count + 1
			addedtask.save()
			new_ownership = Ownership(userProfile=userProfile_obj, task=addedtask)
			new_ownership.save()
			badge_count = userProfile_obj.badges.count()
			check_badges(request, groupie=True)
			if (userProfile_obj.badges.count() > badge_count):
				messages.info(request, "You earned a badge!")
			HttpResponseRedirect(request.path)

		if newid == name:
			profIsUser = True
			owns = Ownership.objects.filter(userProfile=userProfile_obj)
		else:
			other_user = get_object_or_404(UserProfile, name=newid)
			owns = Ownership.objects.filter(userProfile=other_user)
		return render_to_response('profile.html', 
		                          {'owns': owns, 'owntasks':owntasks, 'profPic':profUser.fb_pic, 'badges':badges, 'loggedin':loggedin, 'name':name, 'nameprof':newid, 'profIsUser':profIsUser}, 
		                          context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect('/login/')

def search(request):
	storage = messages.get_messages(request)
	storage.used = True

	if request.user.is_authenticated():
		userProfile_obj = get_object_or_404(UserProfile, user=request.user)
		name = userProfile_obj.name
		loggedin = True

		ownTasks = userProfile_obj.tasks.all()
		tasks = Task.objects.order_by('-count')

		if request.method == 'POST':
			if 'searchTag' in request.POST:
				tagname = request.POST['tagQuery'].lower()
				try:
					tag = Tag.objects.get(tag_text=tagname)
					tasks = Task.objects.filter(tags=tag)
				except Tag.DoesNotExist:
					tasks = None
			elif 'addtaskbutton' in request.POST:
				taskTxt = request.POST['addtaskbutton']
				addedtask = get_object_or_404(Task, task_text=taskTxt)
				addedtask.count = addedtask.count + 1
				addedtask.save()
				new_ownership = Ownership(userProfile=userProfile_obj, task=addedtask)
				new_ownership.save()

		return render_to_response('search.html',
			{'tasks': tasks, 'loggedin':loggedin, 'name':name, 'owntasks':ownTasks}, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/login/')


def check_badges(request, groupie):

	if request.user.is_authenticated():
		userProfile_obj = get_object_or_404(UserProfile, user=request.user)		
		earned_badges = userProfile_obj.badges.all()

		# Doer of Things: Complete 10 tasks.
		try:
			badge = Badge.objects.get(badge_title="Doer of Things")
			if badge not in earned_badges:
				completed_tasks = Ownership.objects.filter(userProfile=userProfile_obj).filter(completed=True)
				if len(completed_tasks) + 1 > 9:
					userProfile_obj.badges.add(badge)
					userProfile_obj.save()	
		except Badge.DoesNotExist:
			pass

		# Groupie: Add a friend's task.
		try:
			badge = Badge.objects.get(badge_title="Groupie")
			if badge not in earned_badges:
				if groupie:
					userProfile_obj.badges.add(badge)
					userProfile_obj.save()	
		except Badge.DoesNotExist:
			pass

		# Sampler: Complete tasks with 5 different tags.
		try:
			badge = Badge.objects.get(badge_title="Sampler")
			if badge not in earned_badges:
				tags = set()
				completed_tasks = Ownership.objects.filter(userProfile=userProfile_obj).filter(completed=True)
				for task in completed_tasks:
					task_tags = task.task.tags.all()
					for tag in task_tags:
						tags.add(tag)
				if len(tags) + 1 > 4:
					userProfile_obj.badges.add(badge)
					userProfile_obj.save()					

		except Badge.DoesNotExist:
			pass

	else:
		return HttpResponseRedirect('/login/')