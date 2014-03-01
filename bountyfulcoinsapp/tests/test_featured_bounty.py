import os

from django_webtest import WebTest

from bountyfulcoinsapp.models import FeaturedBounty, Address
from bountyfulcoinsapp.forms import BountySaveForm

from .common import SiteDataMixin
from .test_bounty import BountyCreateMixin


class TestFeaturedBounty(BountyCreateMixin, SiteDataMixin, WebTest):
    fixtures = ['users', 'bounties', 'addresses']

    def setUp(self):
        super(TestFeaturedBounty, self).setUp()
        self.good_data['featured'] = True

    def test_no_assignable_addresses(self):
        Address.objects.get(verified_balance=0.00).delete()  # remove available
        create_form = self._get_bounty_form()
        self._fill_form(create_form, self.good_data)
        res = create_form.submit()
        self.assertFormError(res, 'form', 'featured',
                             BountySaveForm.no_addresses_error)

    def _get_featured(self, bounty):
        try:
            return bounty.featured
        except FeaturedBounty.DoesNotExist:
            return None

    def test_create_featured_bounty(self):
        bounty = self._create_bounty(self.good_data)
        self.assertIsNotNone(self._get_featured(bounty),
                             'A featured bounty does not exist')

    def test_featured_bounty_enabled(self):
        bounty = self._create_bounty(self.good_data)
        self.assertIsNotNone(self._get_featured(bounty),
                             'A featured bounty does not exist')
        self.assertFalse(bounty.featured.enabled,
                         'Feature should not be enabled')

        bounty.featured.address.verified_balance = 2.0
        self.assertTrue(bounty.featured.enabled, 'Feature should be enabled')

    def test_sync_address_balance(self):
        addr = Address.objects.get(verified_balance__gt=0)
        self.assertEqual(addr.verified_balance, 1.00)

        # force sync_verified_balance to return what we want
        os.environ['TEST_BLOCKCHAIN_BALANCE'] = '2.0'
        self.assertTrue(addr.sync_verified_balance())
        addr = Address.objects.get(pk=addr.pk)  # fetch again
        self.assertEqual(addr.verified_balance, 2.00)
        os.environ.pop('TEST_BLOCKCHAIN_BALANCE', None)
