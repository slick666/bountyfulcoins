from django.contrib import admin
from bountyfulcoinsapp.models import Link, Tag, Address, Bounty, SharedBounty


class BountyAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'user', 'amount', 'currency')
    list_fitler = ('user',)
    ordering = ('title',)
    search_fields = ('title', )


class AddressAdmin(admin.ModelAdmin):
    list_display = ('address_id', 'name', 'verified_balance', 'last_synced')
    list_fitler = ('last_synced',)
    ordering = ('verified_balance',)
    search_fields = ('address_id', 'name',)


admin.site.register(Link)
admin.site.register(Tag)
admin.site.register(Address, AddressAdmin)
admin.site.register(Bounty, BountyAdmin)
admin.site.register(SharedBounty)
