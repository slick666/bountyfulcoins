from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from django_webtest import WebTest

from .common import SiteDataMixin


class TestBountyCreate(SiteDataMixin, WebTest):
    """
    End to end test of the bounty create form, view and template.
    """
    required_fields = ['url', 'title']
    good_data = {
        'url': 'http://example.com/mybounty',
        'title': 'a test bounty',
        'amount': 1.5432,  # defaults to 0.0
        'currency': 'DOGE',  # defaults to BTC
        'tags': 'quick,bounty   , jumped',  # defaults to empty
        'share': False,  # defaults to False
    }
    min_data = dict((k, v) for k, v in good_data.iteritems()
                    if k in required_fields)

    def setUp(self):
        self.create_bounty = self.app.get(reverse('create_bounty'))
        self.create_form = self.create_bounty.form

    def test_bounty_defaults(self):
        self._fill_form(self.create_form, self.min_data)
        res = self.create_form.submit()
        # self.assertIn()
