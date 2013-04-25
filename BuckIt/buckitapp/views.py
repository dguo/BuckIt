# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from models import Tag, Task, User, Ownership

def home(request):
	userId = "Molly Nacey" #we should be able to get user info from login
	user_obj = get_object_or_404(User, name=userId)
	owns = Ownership.objects.filter(user=user_obj).order_by('-date_set').order_by('completed')

	topTasks = Task.objects.order_by('count')[0:3]

	return render_to_response('home.html',
		{'topTasks':topTasks, 'owns':owns},
		context_instance = RequestContext(request))

def login(request):
	return render_to_response('login.html', context_instance=RequestContext(request))

def profile(request, userid):
	newid = userid.replace('_',' ')

	user_obj = get_object_or_404(User, name=newid)
	owns = Ownership.objects.filter(user=user_obj)

	return render_to_response('profile.html', 
	    {'owns': owns}, 
		context_instance = RequestContext(request))

def search(request):
	if request.method == 'POST':
		tagname = request.POST['tagQuery']
		try:
			tag = Tag.objects.get(tag_text=tagname)
			tasks = Task.objects.filter(tags=tag)
		except Tag.DoesNotExist:
			tasks = None
	else:
		tasks = Task.objects.all()
	return render_to_response('search.html',
		{'tasks': tasks}, context_instance=RequestContext(request))

