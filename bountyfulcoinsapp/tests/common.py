

class SiteDataMixin(object):
    fixtures = ['users', 'bounties']
    # existing users: admin | qwe123, test | test

    def _fill_form(self, form, data):
        for field, value in data.iteritems():
            form[field] = value
