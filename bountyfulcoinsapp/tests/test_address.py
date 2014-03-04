import mock
from datetime import timedelta

from django.conf import settings
from django.test import TestCase
from django.utils import timezone

from bountyfulcoinsapp.models import Address


class TestAddressMethods(TestCase):
    fixtures = ['addresses']

    def setUp(self):
        self.addr1 = Address.objects.get(id=1)
        self.addr2 = Address.objects.get(id=2)

    def test_sync_required(self):
        with mock.patch('django.conf.settings.ADDRESSES_LIVE_SYNC', False):
            self.assertFalse(self.addr1.sync_required,
                             "Sync should not be required")

        old_sync = timezone.now() - timedelta(
            settings.ADDRESSES_SYNC_FREQUENCE + 1)
        self.addr2.last_synced = old_sync
        self.assertTrue(self.addr2.sync_required, "Sync should be required")

        future_sync = timezone.now() + timedelta(minutes=1)
        self.addr2.last_synced = future_sync
        self.assertFalse(self.addr2.sync_required,
                         "Sync should not be required")

    def test_bulk_create(self):
        # this data should add 1 address (1 is dupe)
        data = [{
            "name": "test address 2",
            "address_id": "2222222222222222"
        }, {
            "name": "test address",
            "address_id": "asdfgqwert12345"
        }]
        first_count = Address.objects.count()
        Address.bulk_create(addr_list=data)
        self.assertEqual(Address.objects.count(), first_count + 1,
                         "An address should have been added")
