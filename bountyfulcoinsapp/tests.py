from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from django_webtest import WebTest

from bountyfulcoinsapp.forms import RegistrationForm


class TestPageLinks(WebTest):
    def test_header_contains_links(self):
        index = self.app.get(reverse('main_page'))


class TestRegistration(WebTest):
    fixtures = ['users', 'bounties']
    # existing users: admin | qwe123, user | test

    required_fields = ['username', 'email', 'password1', 'password2',
                       'recaptcha_challenge_field']
    good_reg_data = {
        'username': 'test2',
        'email': 'test2@example.com',
        'password1': 'test123',
        'password2': 'test123',
        'recaptcha_challenge_field': 'PASSED'
    }
    extra_environ = {'RECAPTCHA_TESTING': 'True'}  # default to passing

    @classmethod
    def setUpClass(cls):
        cls.User = get_user_model()

    def test_registration_link_work(self):
        index = self.app.get(reverse('main_page'))
        self.assertIn('User Registration', index.click(
            href=reverse('registration_register')))

    def test_registration_fields(self):
        reg_page = self.app.get(reverse('registration_register'))
        reg_form = reg_page.form
        for field in self.required_fields:
            self.assertIn(field, reg_form.fields)

    def _fill_form(self, form, data):
        for field, value in data.iteritems():
            form[field] = value

    def test_all_fields_are_required(self):
        for field in self.required_fields:
            regdata = self.good_reg_data.copy()
            regdata.pop(field)
            reg_page = self.app.get(reverse('registration_register'))
            regform = reg_page.form
            self._fill_form(regform, regdata)
            if field == 'recaptcha_challenge_field':
                continue  # tested seperately below
            self.assertIn(field, RegistrationForm.base_fields)
            original_field = RegistrationForm.base_fields[field]
            req_msg = unicode(original_field.error_messages['required'])
            self.assertFormError(regform.submit(), 'form', field, [req_msg])

    def test_bad_recaptcha(self):
        pass

    def test_username_taken(self):
        reg_page = self.app.get(reverse('registration_register'))
