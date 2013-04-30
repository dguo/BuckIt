# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from models import Tag, Task, UserProfile, Ownership
from django.contrib.auth import authenticate 
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.models import User
import itertools

def home(request):

	username = "Molly" # we should be able to get user info from login
	password = "Molly"

	user = authenticate(username=username, password=password)

	if user is not None:
		
		if user.is_active:
			
			auth_login(request, user)

			if request.user.is_authenticated():

				userProfile_obj = get_object_or_404(UserProfile, user=user)

				if request.method == 'POST':
					print request.POST['task']
					print request.POST['tags']
					# create the new tag task if it doesn't exist already
					new_tag = Tag.objects.filter(tag_text = (request.POST['tags']).lower())
					if len(new_tag) == 1:
						new_tag = new_tag[0]
					else:
						new_tag = Tag(tag_text=request.POST['tags'])
						new_tag.save()	
					# create the new task if it doesn't exist already
					new_task = Task.objects.filter(task_text = request.POST['task'])
					if len(new_task) == 1:
						pass
					else:
						new_task = Task(task_text = request.POST['task'])
						new_task.save()
						new_task.tags.add(new_tag)
						new_ownership = Ownership(userProfile = userProfile_obj, task = new_task)
						new_ownership.save()

					return HttpResponseRedirect('')

				else:	
					owns1 = Ownership.objects.filter(userProfile=userProfile_obj).filter(completed=False).order_by('-date_set')
					owns2 = Ownership.objects.filter(userProfile=userProfile_obj).filter(completed=True).order_by('-date_done')
					owns = itertools.chain(owns1, owns2)
					topTasks = Task.objects.order_by('count')[0:3]
					return render_to_response('home.html',
					                          {'topTasks':topTasks, 'owns':owns},
					                          context_instance = RequestContext(request))	

		else:
			# Return a 'disabled account' error message
			pass
	else:
		# Return an 'invalid login' error message
		pass

	

def login(request):
	logout(request)
	return render_to_response('login.html', context_instance=RequestContext(request))

def profile(request, userid):
	#newid = userid.replace('_',' ')

	if request.user.is_authenticated():
		userProfile_obj = get_object_or_404(UserProfile, user=request.user)
		owns = Ownership.objects.filter(userProfile=userProfile_obj)
		return render_to_response('profile.html', 
		                          {'owns': owns}, 
		                          context_instance = RequestContext(request))
	else:
		return render_to_response('login.html', context_instance=RequestContext(request))

def search(request):
	if request.method == 'POST':
		tagname = request.POST['tagQuery'].lower()
		try:
			tag = Tag.objects.get(tag_text=tagname)
			tasks = Task.objects.filter(tags=tag)
		except Tag.DoesNotExist:
			tasks = None
	else:
		tasks = Task.objects.all()
	return render_to_response('search.html',
		{'tasks': tasks}, context_instance=RequestContext(request))