from django.shortcuts import render
from django.http.response import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
from post.models import Post, Comments
# Create your views here.

def basic_one(request):
	view = "basic_one"
	html = "<html><body>this is %s view</body><html>" % view
	return HttpResponse(html)

def template_two(request):
	view = "template_two"
	t=get_template('myview.html')
	html = t.render(Context({'name':view}))
	return HttpResponse(html)

def template_three_simple(request):
	view = "template_three"
	return render_to_response('myview.html', {'name': view})

def posts(request):
	return render_to_response('posts.html', {'posts': Post.objects.all()})

def posts_of_user(request, user_id):
	return render_to_response('posts.html', {'posts': Post.objects.filter(post_id=user_id)})