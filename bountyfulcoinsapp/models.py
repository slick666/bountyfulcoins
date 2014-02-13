from django.db import models, connection
print connection.queries
from django.contrib.auth.models import User

# Create your models here.
class Link(models.Model):
	url = models.URLField(unique=True)
	def __unicode__(self):
		return self.url

class Bounty(models.Model):
	title = models.CharField(max_length=200)
	user = models.ForeignKey(User)
	link = models.ForeignKey(Link)
#	amount = models.DecimalField(max_digits=20,decimal_places=8)
#	currency = models.CharField(max_length=3)
#	description = models.TextField()
	def __unicode__(self):
		return u'%s, %s, %s, %s, %s' % (self.user.username, self.link.url, 
			self.amount, self.currency, self.description)

class Tag(models.Model):
	name = models.CharField(max_length=64, unique=True)
	bounties = models.ManyToManyField(Bounty)
	def __unicode__(self):
		return self.name

class SharedBounty(models.Model):
	bounty = models.ForeignKey(Bounty, unique=True)
	date = models.DateTimeField(auto_now_add=True)
	votes = models.IntegerField(default=1)
	users_voted = models.ManyToManyField(User)
	def __unicode__(self):
		return u'%s, %s' % (self.bounty, self.votes)