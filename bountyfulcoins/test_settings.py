try:
    from host_settings import *
except ImportError:
    from settings import *


DATABASES = {
    'default': {
        # Use sqlite for faster testing
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'bountyfulcoins/bountyfulcoins.test.db',
    }
}
