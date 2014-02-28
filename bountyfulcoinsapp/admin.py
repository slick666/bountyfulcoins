from django.contrib import admin
from bountyfulcoinsapp.models import *


# Link Model
class LinkAdmin(admin.ModelAdmin):
    pass
admin.site.register(Link, LinkAdmin)


# Bounty Model
class BountyAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'user', 'amount', 'currency')
    list_fitler = ('user',)
    ordering = ('title',)
    search_fields = ('title', )
admin.site.register(Bounty, BountyAdmin)


# Tag Model
class TagAdmin(admin.ModelAdmin):
    pass
admin.site.register(Tag, TagAdmin)


# Shared Bounty
class SharedBountyAdmin(admin.ModelAdmin):
    pass
admin.site.register(SharedBounty, SharedBountyAdmin)
