# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
#from BuckIt.buckitapp import Tag, Task, User, Ownership

def home(request):
	return render_to_response('home.html')

def login(request):
	return render_to_response('login.html', context_instance=RequestContext(request))

def profile(request, userid):

	tasks = ownerships.objects.filter(user=userid)

	return render_to_response('profile.html', 
	    {'tasks': tasks}, 
		context_instance = RequestContext(request))

