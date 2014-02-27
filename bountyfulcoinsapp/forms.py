from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from captcha.fields import ReCaptchaField
from registration.forms import RegistrationForm as BaseRegistrationForm
from validate_email import validate_email

from bountyfulcoinsapp.models import Bounty


class RegistrationForm(BaseRegistrationForm):
    recaptcha = ReCaptchaField(attrs={'theme': 'clean'})

    def clean_email(self):
        """ Validate that the supplied email address does not exist """
        User = get_user_model()
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_(
                "This email address is already in use. Please supply a "
                "different email address."))
        if not validate_email(self.cleaned_data['email'],
                              check_mx=settings.CHECK_MX,
                              verify=settings.CHECK_EMAIL_EXISTS):
            raise forms.ValidationError(_(
                "This email does not seem to be a valid address, please try"
                " another mail address"))
        return self.cleaned_data['email']


class BountySaveForm(forms.ModelForm):
    class Meta:
        model = Bounty
        exclude = ('link', 'user',)
        fields = ('url', 'title', 'amount', 'currency', 'tags', 'share')

    url = forms.URLField(
        label=u'Bounty URL',
        widget=forms.TextInput(attrs={'size': 128}),
    )
    tags = forms.CharField(
        label=u'Tags',
        required=False,
        widget=forms.TextInput(attrs={'size': 64}),
        help_text=_('Please enter a comma seperated list of tags')
    )
    share = forms.BooleanField(
        label=u'Post to Bountyful Home Page',
        required=False
    )


class SearchForm(forms.Form):
    query = forms.CharField(
        label=u'Enter a keyword to search bounties',
        widget=forms.TextInput(attrs={'size': 32})
    )
