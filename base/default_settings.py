class Config(object):
    DEBUG = True
    SECRET_KEY = 'SECRET-THIS-SHOULD-BE-CHANGED'
    SQLALCHEMY_DATABASE_URI  = 'mysql://hootenflaten_user@127.0.0.1/hootenflaten'
    SECURITY_PASSWORD_HASH = 'bcrypt'

    SITE_SETTINGS = {
      'SHORT_NAME'      : 'Hooten',
      'FULL_NAME'       : "HootenFlaten: Social in a Box",
      'FACEBOOK_AUTH'   : True
    }

    FACEBOOK = {
        'ID' : 'FACEBOOK_SECRET_ID',
        'SECRET' : 'FACEBOOK_SECRET_KEY',
        'REDIRECT_URI': 'http://idev.hootenflaten.org:5000/facebook/complete',
        'SCOPES': [
            'user_about_me',
            'user_birthday',
            'user_checkins',
            'user_education_history',
            'user_events',
            'user_hometown',
            'user_groups',
            'user_photos',
            'user_relationships',
            'user_status',
            'friends_about_me',
            'friends_birthday',
            'friends_checkins',
            'friends_education_history',
            'friends_events',
            'friends_hometown',
            'friends_groups',
            'friends_photos',
            'friends_relationships',
            'friends_status',
            'email',
            'create_event',
            'rsvp_event',
            ]
    }

    EXTENSIONS = list(['hootenflaten_auth', 'hootenflaten_status'])
    EXTENSIONS.append('facebook_auth')
