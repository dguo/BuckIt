# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext

def home(request):
	return render_to_response('home.html')

def login(request):
	return render_to_response('login.html', context_instance=RequestContext(request))

def profile(request, userid):
	return render_to_response('profile.html')# Create your views here.
