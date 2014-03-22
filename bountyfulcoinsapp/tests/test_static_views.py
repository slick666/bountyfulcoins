from django.core.urlresolvers import reverse

from django_webtest import WebTest

from .common import SiteDataMixin


class TestHeaderLinks(SiteDataMixin, WebTest):
    required_links = ('main_page',
                      'popular',
                      'about',)
    logged_out = ('auth_login',
                  'registration_register',)
    logged_in = ('auth_logout', 'create_bounty',)

    def test_header_contains_links(self):
        # logged out test
        index = self.app.get(reverse('main_page'))
        for link in self.required_links + self.logged_out:
            self.assertTrue(index.click(href=reverse(link), index=0))

        # authenticated test
        index = self.app.get(reverse('main_page'), user='user')
        for link in self.required_links + self.logged_in:
            self.assertTrue(index.click(href=reverse(link), index=0))

        self.assertTrue(index.click(href=reverse(
            'user_page', args=['user']), index=0))
