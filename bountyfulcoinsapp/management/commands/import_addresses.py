import csv

from django.core.management.base import LabelCommand

from bountyfulcoinsapp.models import Address


class Command(LabelCommand):
    help = "Accepts csv files of address lists and inserts them into database"
    args = "<file1.csv file2.csv ...>"
    label = 'file'

    def handle_label(self, filename, **options):
        addresses = []
        with open(filename, 'rbU') as csvfile:
            for addr in csv.DictReader(csvfile, fieldnames=(
                    '_', 'address_id')):
                del addr['_']
                addresses.append(addr)
        Address.bulk_create(addresses)
