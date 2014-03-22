import os

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from django_webtest import WebTest

from bountyfulcoinsapp.forms import RegistrationForm
from .common import SiteDataMixin


class TestRegistration(SiteDataMixin, WebTest):
    """
    End to end test of the registration form, view and templates
    """
    required_fields = ['username', 'email', 'password1', 'password2',
                       'recaptcha_response_field']
    good_reg_data = {
        'username': 'test2',
        'email': 'test2@example.com',
        'password1': 'test123',
        'password2': 'test123',
        'recaptcha_response_field': 'PASSED'
    }

    def setUp(self):
        os.environ['RECAPTCHA_TESTING'] = 'True'

    def tearDown(self):
        os.environ.pop('RECAPTCHA_TESTING', None)

    def test_registration_link_work(self):
        index = self.app.get(reverse('main_page'))
        self.assertIn('User Registration', index.click(
            href=reverse('registration_register')))

    def test_registration_fields(self):
        reg_page = self.app.get(reverse('registration_register'))
        reg_form = reg_page.forms['reg-form']
        for field in self.required_fields:
            self.assertIn(field, reg_form.fields)

    def _get_filled_form(self, field_name, value=None):
        reg_page = self.app.get(reverse('registration_register'))
        regform = reg_page.forms['reg-form']
        data = self.good_reg_data.copy()
        if value:
            data[field_name] = value
        else:
            data.pop(field_name)
        self._fill_form(regform, data)
        return regform

    def test_all_fields_are_required(self):
        for field in self.required_fields:
            regform = self._get_filled_form(field)
            if field == 'recaptcha_response_field':
                continue  # tested seperately below
            self.assertIn(field, RegistrationForm.base_fields)
            original_field = RegistrationForm.base_fields[field]
            req_msg = unicode(original_field.error_messages['required'])
            self.assertFormError(regform.submit(), 'form', field, req_msg)

    def test_bad_captcha(self):
        field_name = 'recaptcha'
        regform = self._get_filled_form('recaptcha_response_field', 'FAILED')
        original_field = RegistrationForm.base_fields[field_name]
        err_msg = unicode(original_field.error_messages['captcha_invalid'])
        self.assertFormError(regform.submit(), 'form',
                             field_name, err_msg)

    def test_username_taken(self):
        regform = self._get_filled_form('username', 'test')
        err_msg = _("A user with that username already exists.")
        self.assertFormError(regform.submit(), 'form',
                             'username', err_msg)

    def test_username_invalid(self):
        field_name = 'username'
        regform = self._get_filled_form(field_name, 'user~[]sql=0>')
        original_field = RegistrationForm.base_fields[field_name]
        err_msg = unicode(original_field.error_messages['invalid'])
        self.assertFormError(regform.submit(), 'form', field_name,
                             err_msg)

    def test_email_taken(self):
        field_name = 'email'
        regform = self._get_filled_form(field_name, 'user@example.com')
        err_msg = RegistrationForm.email_taken_error
        self.assertFormError(regform.submit(), 'form', field_name,
                             err_msg)

    def test_valid_registration(self):
        reg_page = self.app.get(reverse('registration_register'))
        regform = reg_page.forms['reg-form']
        self._fill_form(regform, self.good_reg_data)
        success = regform.submit()
        self.assertRedirects(success, reverse('registration_complete'))

    def test_registration_unavailable_to_user(self):
        # TODO: write me
        self.skipTest("Not Implemented")
