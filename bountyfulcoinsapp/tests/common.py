from django.contrib.auth import get_user_model


class SiteDataMixin(object):
    fixtures = ['users', 'bounties']
    # existing users: admin | qwe123, user | test

    @classmethod
    def setUpClass(cls):
        cls.User = get_user_model()
