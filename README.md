# Bountyful Coins Bounty Directory

### App version 0.2

[![Build Status](https://travis-ci.org/asfaltboy/bountyfulcoins.png?branch=registration)](https://travis-ci.org/asfaltboy/bountyfulcoins)


## Deployment

1. Clone this repository
2. (optional) Create [a virtualenv](http://www.virtualenv.org/en/latest/virtualenv.html); source into the virtualenv.
3. Install [requirements](http://www.pip-installer.org/en/1.1/requirements.html) by running `pip install -r requirements.txt`
4. Set up host specific settings in a custom settings module (for an example of new available settings to override - with their defaults, see below)
5. run the following set of django management commands:
    1. `python manage.py syncdb --noinput`
    2. `python manage.py migrate`
    3. `python manage.py collectstatic --noinput`
    4. `python manage.py compilemessages`

### Settings (i.e: a `host_settings.py` file)

    from settings import *

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'bountyfulcoins.staging.db',
        }
    }

    ACCOUNT_ACTIVATION_DAYS = 7  # One-week activation window
    RECAPTCHA_USE_SSL = True

    # replace with a real key pair from here:
    # http://www.google.com/recaptcha/whyrecaptcha
    RECAPTCHA_PUBLIC_KEY = 'THIS_SHOULD_BE_A_REAL_KEY'
    RECAPTCHA_PRIVATE_KEY = 'THIS_SHOULD_BE_A_REAL_KEY'

    # an issue with pydns prevents this from working properly
    CHECK_MX = False
    CHECK_EMAIL_EXISTS = False

    FEATURE_POST_MIN_CHARGE = 0.01594
    FEATURE_POST_DAILY_CHARGE = 0.01594

    ADDRESSES_LIVE_SYNC = True  # turn this off when running sync in cron
    ADDRESSES_SYNC_FREQUENCE = 60 * 5  # five minutes

### Running Tests

To run the test suite, simply run:

    python manage.py test --settings=bountyfulcoins.test_settings
