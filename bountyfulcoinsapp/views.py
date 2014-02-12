from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpRequest 
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
	shared_bounties = SharedBounty.objects.order_by('-date')[:50]
	variables = RequestContext(request, {
		'shared_bounties': shared_bounties
		})
	return render_to_response('main_page.html', variables)

# View of the User Page.
def user_page(request, username): 
	user = get_object_or_404(User, username=username)
	bounties = user.bounty_set.order_by('-id')
	variables = RequestContext(request, {
		'bounties': bounties,
		'username': username, 
		'show_tags': True,
		'show_edit': username == request.user.username,
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
	# ajax = 'ajax' in request.GET
	ajax = request.is_ajax()
	if request.method == 'POST':
		form = BountySaveForm(request.POST)
		if form.is_valid():
			bounty = _bounty_save(request, form)
			if ajax:
				variables = RequestContext(request, {
					'bounties': [bounty],
					'show_edit': True,
					'show_tags': True
					})
				return render_to_response(
					'bounty_list.html', variables
				)
			else:
				return HttpResponseRedirect(
				'/user/%s/' % request.user.username
				)
		else:
			if ajax:
				return HttpResponse(u'Javascript failure')
	elif 'url' in request.GET:
		url = request.GET['url']
		title = ''
		tags = ''
		try:
			link = Link.objects.get(url=url)
			bounty = Bounty.objects.get(
				link=link,
				user=request.user
			)
			title = bounty.title
			tags = ' '.join(
				tag.name for tag in bounty.tag_set.all()
			)
		except (Link.DoesNotExist, Bounty.DoesNotExist):
			pass
		form = BountySaveForm({
			'url': url,
			'title': title,
			'tags': tags
		})
	else:
		form = BountySaveForm()
	variables = RequestContext(request, {
		'form': form
	})
	if ajax:
		return render_to_response('bounty_save.html', variables)
	else:
		return render_to_response('bounty_save.html', variables)



def _bounty_save(request, form):
	# Create or get link
	link, dummy = Link.objects.get_or_create(
		url=form.cleaned_data['url']
	)
	# Create or get Bounty.
	bounty, created = Bounty.objects.get_or_create(
		user=request.user,
		link=link
	)
	# Update Bounty title.
	bounty.title = form.cleaned_data['title']
	# If the bounty is being updated, clear old tag list
	if not created:
		bounty.tag_set.clear()	
	# Create new tag list
	tag_names = form.cleaned_data['tags'].split()
	for tag_name in tag_names:
		tag, dummy = Tag.objects.get_or_create(name=tag_name)
		bounty.tag_set.add(tag)
	# Post on the Home page if requested
	if form.cleaned_data['share']:
		shared, created = SharedBounty.objects.get_or_create(
			bounty=bounty
	)
	if created:
		shared.users_voted.add(request.user)
		shared.save() 
	# Save the Bounty to the database and return it.
	bounty.save()
	return bounty


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

def search_page(request):
	form = SearchForm()
	bounties = []
	show_results = False
	if 'query' in request.GET:
		show_results = True
		query = request.GET['query'].strip()
		if query:
			form = SearchForm({'query' : query})
			bounties = Bounty.objects.filter(
				title__icontains=query
			)[:10]
	variables = RequestContext(request, {
		'form': form,
		'bounties': bounties,
		'show_results': show_results,
		'show_tags': True,
		'show_user': True
	})
	if request.GET.has_key('ajax'):
		return render_to_response('bounty_list.html', variables)
	else:
		return render_to_response('search.html', variables)