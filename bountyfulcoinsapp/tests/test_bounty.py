from django.core.urlresolvers import reverse

from django_webtest import WebTest

from bountyfulcoinsapp.models import Bounty
from .common import SiteDataMixin


class BountyCreateMixin(object):
    default_data = {
        'amount': 0.00,
        'currency': 'BTC',
    }
    good_data = {
        'url': 'http://example.com/my_new_bounty',
        'title': 'a test bounty',
        'amount': 1.54,  # defaults to 0.00
        'currency': 'DOGE',  # defaults to BTC
        'tags': '',  # defaults to empty
        'share': False,  # defaults to False
    }

    def setUp(self):
        self.create_url = reverse('create_bounty')

    def _get_bounty_form(self, new=False):
        create_bounty = self.app.get(self.create_url, user='user')
        return create_bounty.form

    def _create_bounty(self, data):
        create_form = self._get_bounty_form()
        self._fill_form(create_form, data)
        res = create_form.submit()
        self.assertEqual(res.status_code, 302, msg="Could not create bounty!"
                         " form errors were: \"%s\"" % ", ".join(
                             [err.text for err in res.html.findChildren(
                                 class_='errorlist')])
                         )
        return Bounty.objects.get(link__url=data['url'])


class TestBountyCreate(BountyCreateMixin, SiteDataMixin, WebTest):
    """
    End to end test of the bounty create form, view and template.
    """
    required_fields = ['url', 'title']

    def test_login_required(self):
        res = self.app.get(self.create_url)
        self.assertRedirects(res, "{login_url}?next={create_url}".format(
            login_url=reverse('auth_login'),
            create_url=self.create_url))

    def test_bounty_defaults(self):
        min_data = dict((k, v) for k, v in self.good_data.iteritems()
                        if k in self.required_fields)
        create_form = self._get_bounty_form()
        self._fill_form(create_form, min_data)
        res = create_form.submit()
        b = Bounty.objects.get(link__url=self.good_data['url'])
        self.assertRedirects(res, reverse('change_bounty', args=[b.pk]))

        for field, value in self.default_data.items():
            self.assertEqual(getattr(b, field), value)

        self.assertFalse(b.tags.exists())
        self.assertFalse(b.shared.exists())

    def test_tags(self):
        data = self.good_data.copy()
        data['tags'] = 'quick,bounty   , jumped'
        bounty = self._create_bounty(data)
        self.assertTrue(bounty.tags.filter(name='jumped').exists())

    def test_sharing(self):
        data = self.good_data.copy()
        data['share'] = True
        bounty = self._create_bounty(data)
        self.assertTrue(bounty.shared.exists())

    def test_clean_curency(self):
        data = self.good_data.copy()
        data['currency'] = ' BTC    '
        bounty = self._create_bounty(data)
        self.assertEquals(bounty.currency, data['currency'].strip())
