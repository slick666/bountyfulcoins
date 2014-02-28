try:
    from host_settings import *
except ImportError:
    from settings import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Use sqlite for faster testing
        'NAME': 'bountyfulcoins/bountyfulcoins.test.db',
    }
}
