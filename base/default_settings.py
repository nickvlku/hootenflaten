class Config(object):
    DEBUG = True
    SECRET_KEY = 'SECRET-THIS-SHOULD-BE-CHANGED'
    SQLALCHEMY_DATABASE_URI  = 'mysql://root@127.0.0.1/hootenflaten'

    SECURITY_PASSWORD_HASH = "sha512_crypt"
    SECURITY_PASSWORD_SALT = "SECRET_SALT"

    SECURITY_TRACKABLE = True

    SHORT_NAME = 'Hooten'
    FULL_NAME = 'HootenFlaten: Social in a Box'
    
    FACEBOOK_AUTH = True 
    FACEBOOK_ID = 'FACEBOOK_SECRET_ID'
    FACEBOOK_SECRET = 'FACEBOOK_SECRET_KEY'
    FACEBOOK_REDIRECT_URL = 'http://idev.hootenflaten.org:5000/facebook/callback'
    FACEBOOK_SCOPES =  [
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

    EXTENSIONS = list(['hootenflaten_auth', 'hootenflaten_status', 'hootenflaten_user_profile'])
    EXTENSIONS.append('facebook_auth')
