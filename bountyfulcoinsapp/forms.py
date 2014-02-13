import re
from django import forms
from django.contrib.auth.models import User
from django.db import connection
print connection.queries

class RegistrationForm(forms.Form):
	username = forms.CharField(label=u'Username', max_length=30)
	email = forms.EmailField(label=u'Email')
	password1 = forms.CharField(
		label=u'Password',
		widget=forms.PasswordInput()
	)
	password2 = forms.CharField(
		label=u'Password (Again)',
		widget=forms.PasswordInput()
	)
	
	def cleaned_password2(self):
		if 'password1' in self.cleaned_data:
			password1 = self.cleaned.data['password1']
			password2 = self.cleaned_data['password2']
			if password1 == password2:
				return password2
		raise forms.ValidationError('Passwords do not matrch.')

	def cleaned_username(self):
		username = self.cleaned_data['username']
		if not re.search(r'^w+$', username):
			raise forms.ValidationError('Username can only contain '
				'alphanumeric characters and the underscore.')
			try:
				User.objects.get(username=username)
			except User.DoesNotExist:
				return username
			raise forms.ValidationError('Username is already taken.')

class BountySaveForm(forms.Form):
	url = forms.URLField(
		label=u'Bounty URL',
		widget=forms.TextInput(attrs={'size': 128})
	)
	title = forms.CharField(
		label=u'Bounty Title',
		widget=forms.TextInput(attrs={'size': 64})
	)
#	amount = forms.DecimalField(
#		label=u'Bounty Amount',
#		widget=forms.TextInput(attrs={'size': 20})
#	)
#	currency = forms.CharField(
#		label=u'Bounty Currency',
#		widget=forms.TextInput(attrs={'size': 2})
#	)
#	description = forms.CharField(
#		label=u'Bounty Description',
#		widget=forms.Textarea
#	)
	tags = forms.CharField(
		label=u'Tags',
		required=False,
		widget=forms.TextInput(attrs={'size': 64})
	)
	share = forms.BooleanField(
		label = u'Post to Bountyful Home Page',
		required=False
	)

class SearchForm(forms.Form):
	query = forms.CharField(
		label=u'Enter a keyword to search bounties',
		widget=forms.TextInput(attrs={'size': 32})
)