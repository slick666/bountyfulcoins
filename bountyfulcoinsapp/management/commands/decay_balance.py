import logging

from django.core.management.base import BaseCommand

from bountyfulcoinsapp.models import Address


logger = logging.getLogger('bountyfulcoinsapp.%s' % __name__)


class Command(BaseCommand):
    help = "Iterate over Addresses tied to FeaturedBounties and sync them"

    def handle(self, *args, **options):
        for addr in Address.objects.exclude(featured_bounty=None):
            logger.info('Syncing balance for address %s', addr.address_id)
            addr.sync_verified_balance()
