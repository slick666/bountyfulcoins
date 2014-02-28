from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Link(models.Model):
    url = models.URLField(unique=True)

    def __unicode__(self):
        return self.url


class Bounty(models.Model):
    link = models.ForeignKey(Link, verbose_name=_('Bounty URL'))
    title = models.CharField(_('Bounty Title'), max_length=200)
    user = models.ForeignKey(get_user_model())
    amount = models.DecimalField(_('Bounty Amount'), default=0.00,
                                 max_digits=20, decimal_places=2)
    currency = models.CharField(_('Bounty Currency'), default='BTC',
                                max_length=15)
#	description = models.TextField()

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
    bounty = models.ForeignKey(Bounty, unique=True, related_name='shared')
    date = models.DateTimeField(auto_now_add=True)
    votes = models.IntegerField(default=1)
    users_voted = models.ManyToManyField(get_user_model())

    disabled = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s, %s' % (self.bounty, self.votes)
