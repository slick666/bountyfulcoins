from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, get_object_or_404
from bountyfulcoinsapp.forms import *
from bountyfulcoinsapp.models import *


# Views for the Home Page
def main_page(request):
	return render_to_response(
		'main_page.html', RequestContext(request)
)

# View of the User Page.
def user_page(request, username): 
	user = get_object_or_404(User, username=username)
	bounties = user.bounty_set.order_by('-id')
	variables = RequestContext(request, {
		'bounties': bounties,
		'username': username, 
		'show_tags': True
	})
	return render_to_response('user_page.html', variables)

# View for the Logout Page
def logout_page(request):
	logout(request)
	return HttpResponseRedirect('/')

# View for the user registration page
def register_page(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(
				username=form.cleaned_data['username'],
				password=form.cleaned_data['password1'],
				email=form.cleaned_data['email']
			)
			return HttpResponseRedirect('/register/success')
	else:
		form = RegistrationForm()
	variables = RequestContext(request, {
		'form': form
		})
	return render_to_response(
		'registration/register.html',
		variables
		) 

# View for the Bounty Save Page very similar to the registration page view above
@login_required
def bounty_save_page(request):
	if request.method == 'POST':
		form = BountySaveForm(request.POST)
		if form.is_valid():
			# Create or get link
			link, dummy = Link.objects.get_or_create(
				url=form.cleaned_data['url']
			)
			# Create or get Bounty.
			bounty, created = Bounty.objects.get_or_create(
				user=request.user,
				link=link
			)
			#Update Bounty title.
			bounty.title = form.cleaned_data['title']
			#if the bounty is being updated, clear old tag list
			if not created:
				bounty.tag_set.clear()
				#Create new tag list
				tag_names = form.cleaned_data['tags'].split()
				for tag_name in tag_names:
					tag, dummy = Tag.objects.get_or_create(name=tag_name)
					bounty.tag_set.add(tag)
				# Save the Bounty to the database.
				bounty.save()
				return HttpResponseRedirect(
					'/user/%s/' % request.user.username
				)
	else:
		form = BountySaveForm()
	variables = RequestContext(request, {
		'form': form
	})
	return render_to_response('bounty_save.html', variables)

def tag_page(request, tag_name):
	tag = get_object_or_404(Tag, name=tag_name)
	bounties = tag.bounties.order_by('-id')
	variables = RequestContext(request, {
		'bounties': bounties,
		'tag_name': tag_name,
		'show_tags': True,
		'show_user': True
	})
	return render_to_response('tag_page.html', variables)

def tag_cloud_page(request):
	MAX_WEIGHT = 5
	tags = Tag.objects.order_by('name')
	#Calculate tag, minimum and maximum counts.
	min_count = max_count = tags[0].bounties.count()
	for tag in tags:
		tag.count = tag.bounties.count()
		if tag.count < min_count:
			min_count = tag.count
		if max_count < tag.count:
			max_count = tag.count
	#Calculate count range. Avoid dividing by zero
	range = float(max_count - min_count)
	if range == 0.0:
		range = 1.0
	# Calculate the tag weights.
	for tag in tags:
		tag.weight = int(
			MAX_WEIGHT * (tag.count - min_count) / range
		)
	variables = RequestContext(request, {
		'tags': tags
	})
	return render_to_response('tag_cloud_page.html', variables)