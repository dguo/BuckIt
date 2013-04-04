# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext

def list(request, title):
	list_name = title.replace('_',' ')
	return render_to_response('list.html',
		{'list_name': list_name,})