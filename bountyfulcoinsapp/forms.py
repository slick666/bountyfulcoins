from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from captcha.fields import ReCaptchaField
from registration.forms import RegistrationForm as BaseRegistrationForm
from validate_email import validate_email

from bountyfulcoinsapp.models import Bounty, Tag, SharedBounty, Link


class RegistrationForm(BaseRegistrationForm):
    recaptcha = ReCaptchaField(attrs={'theme': 'clean'})
    email_taken_error = _("This email address is already in use. Please "
                          "supply a different email address.")
    invalid_email_error = _("This email does not seem to be a valid address, "
                            "please try another mail address")

    def clean_email(self):
        """ Validate that the supplied email address does not exist """
        User = get_user_model()
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(self.email_taken_error)
        if settings.CHECK_MX or settings.CHECK_EMAIL_EXISTS:
            if not validate_email(self.cleaned_data['email'],
                                  check_mx=settings.CHECK_MX,
                                  verify=settings.CHECK_EMAIL_EXISTS):
                raise forms.ValidationError(self.invalid_email_error)
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

    def clean_currency(self):
        # TODO: validate currency is a valid choice ?
        currency = self.cleaned_data['currency']
        return currency.strip()

    def save(self, user=None):
        """
        Parse tags, link and user and create/update links to related models
        """
        if not user:
            raise forms.ValidationError(
                _('Cannot save bouty without a user'))
        data = self.cleaned_data
        bounty = super(BountySaveForm, self).save(commit=False)
        bounty.user = user
        bounty.link, created = Link.objects.get_or_create(url=data['url'])
        tag_names = data['tags'].split(',')

        bounty.save()  # first create this record to allow m2m access

        bounty.tags.clear()  # remove existing tags before assigning new ones
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name.strip())
            bounty.tags.add(tag)

        if data['share']:
            shared, created = SharedBounty.objects.get_or_create(
                bounty=bounty
            )

            if created:
                shared.users_voted.add(user)
        return bounty


class SearchForm(forms.Form):
    query = forms.CharField(
        label=u'Enter a keyword to search bounties',
        widget=forms.TextInput(attrs={'size': 32})
    )
