from django.core.management.base import LabelCommand

from bountyfulcoinsapp.models import Address
from bountyfulcoinsapp.utils import get_addresses_from_file


class Command(LabelCommand):
    help = "Accepts csv files of address lists and inserts them into database"
    args = "<file1.csv file2.csv ...>"
    label = 'file'

    def handle_label(self, filename, **options):
        with open(filename, 'rbU') as csvfile:
            addresses = get_addresses_from_file(
                csvfile, headers=('_', 'address_id'))
        Address.bulk_create(addresses)
