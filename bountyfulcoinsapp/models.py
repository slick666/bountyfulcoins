from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from blockchain_adapter import blockchain


class Link(models.Model):
    url = models.URLField(unique=True)

    def __unicode__(self):
        return self.url


class Bounty(models.Model):
    class Meta:
        verbose_name_plural = 'Bounties'

    link = models.ForeignKey(Link, verbose_name=_('Bounty URL'))
    title = models.CharField(_('Bounty Title'), max_length=200)
    user = models.ForeignKey(get_user_model())
    amount = models.DecimalField(_('Bounty Amount'), default=0.00,
                                 max_digits=20, decimal_places=2)
    currency = models.CharField(_('Bounty Currency'), default='BTC',
                                max_length=15)

    def __unicode__(self):
        return u'%s, %s' % (self.user.username, self.link.url)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('change_bounty', args=[str(self.id)])


class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)
    bounties = models.ManyToManyField(Bounty, related_name='tags')

    def __unicode__(self):
        return self.name


class SharedBounty(models.Model):
    class Meta:
        verbose_name_plural = 'Shared bounties'

    bounty = models.ForeignKey(Bounty, unique=True, related_name='shared')
    date = models.DateTimeField(auto_now_add=True)
    votes = models.IntegerField(default=1)
    users_voted = models.ManyToManyField(get_user_model())

    disabled = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s, %s' % (self.bounty, self.votes)


class Address(models.Model):
    name = models.CharField(max_length=255, blank=True)
    address_id = models.CharField(max_length=64, unique=True)

    verified_balance = models.DecimalField(default=0.00, max_digits=20,
                                           decimal_places=6)
    last_synced = models.DateTimeField(null=True)

    @property
    def sync_required(self):
        if not settings.ADDRESSES_LIVE_SYNC:
            return False
        freq = timedelta(seconds=settings.ADDRESSES_SYNC_FREQUENCE)
        return (datetime.now() - self.last_synced) > freq

    def sync_verified_balance(self):
        """
        Using blockchain.info API get the latest balance of the Address.

        If a good result is returned, store it and update last_synced time.
        """
        res = blockchain.get_balance()
        if res is not None:
            self.verified_balance = res
            self.last_synced = datetime.now()
            self.save()
            return True
        return False


class FeaturedBounty(models.Model):
    class Meta:
        verbose_name_plural = 'Featured bounties'

    shared_bounty = models.OneToOneField(SharedBounty,
                                         related_name='featured')
    address = models.OneToOneField(Address, unique=True,
                                   related_name='featured_bounty')
    ctime = models.DateTimeField(auto_now_add=True)

    @property
    def enabled(self):
        if self.address.verified_balance >= settings.MIN_BTC_FEATURE_POST:
            return True
        elif self.address.last_synced is None or self.address.sync_required:
            res = self.address.sync_verified_balance()
            if res:  # balance was updated, check again
                return self.enabled
        # cannot verify payment was made, return False
        return False
