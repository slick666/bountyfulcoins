import csv


def get_addresses_from_csv(csvfile, headers):
    addresses = []
    for addr in csv.DictReader(csvfile, fieldnames=headers):
        del addr['_']
        addresses.append(addr)
    return addresses
