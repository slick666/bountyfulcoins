from django.core.management.base import BaseCommand

from bountyfulapp.models import Address


class Command(BaseCommand):
    help = "Iterate over Addresses tied to FeaturedBounties and sync them"

    def handle(self, *args, **options):
        for addr in Address.objects.exclude(featured_bounty=None):
            addr.sync_verified_balance()
