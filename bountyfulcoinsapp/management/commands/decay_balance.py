import logging

from django.core.management.base import BaseCommand

from bountyfulcoinsapp.models import Address


logger = logging.getLogger('%s' % __name__)


class Command(BaseCommand):
    help = "Iterate over Addresses tied to FeaturedBounties and sync them"

    def handle(self, *args, **options):
        for addr in Address.objects.exclude(featured_bounty=None):
            logger.info('Syncing balance for address %s', addr.address_id)
            balance = addr.verified_balance
            if addr.sync_verified_balance():
                logger.info('Balance for %s updated from %s to %s',
                            addr.address_id, balance, addr.verified_balance)
            else:
                logger.warn('Balance for %s could not be updated from '
                            'blockchain.info API', addr.address_id)
