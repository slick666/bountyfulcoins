from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from bountyfulcoinsapp.forms import *
from bountyfulcoinsapp.models import *


# Views for the Home Page
def main_page(request):
	return render_to_response(
		'main_page.html', RequestContext(request)
)

# View of the User Page.
def user_page(request, username): 
	try:
		user = User.objects.get(username=username)
	except User.DoesNotExist:
		raise Http404(u'The Requested user was not found.')

	bounties = user.bounty_set.all()

	template = get_template('user_page.html')
	variables = RequestContext(request, {
		'username': username,
		'bounties': bounties
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
			link, dummy = LInk.objects.get_or_create(
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
					tag, dummy = Tagobjects.get_or_create(name=tag_name)
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