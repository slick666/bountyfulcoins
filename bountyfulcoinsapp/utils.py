import logging
import csv

from django.conf import settings

import tweepy

logger = logging.getLogger('bountyfulcoinsapp.utils')


def get_addresses_from_csv(csvfile, headers):
    addresses = []
    for addr in csv.DictReader(csvfile, fieldnames=headers):
        del addr['_']
        addresses.append(addr)
    return addresses


def get_protocol(request):
    if request is not None and request.is_secure():
        return u'https://'
    return u'http://'


def get_authenticated_twitter_api():
    logger.debug('Authenticating with twitter API')
    auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY,
                               settings.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(settings.TWITTER_ACCESS_TOKEN,
                          settings.TWITTER_ACCESS_TOKEN_SECRET)

    return tweepy.API(auth)
