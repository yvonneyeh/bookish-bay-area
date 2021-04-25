import os

class Config:

    MAPS_JS_KEY = os.environ['MAPS_JS_KEY']
    MAPS_GEOCODING_KEY = os.environ['MAPS_GEOCODING_KEY']
    MAP_ID = os.environ['MAP_ID']
    MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
    SENDGRID_API_KEY = os.environ['SENDGRID_API_KEY']
    DATABASE_URL = os.environ['DATABASE_URL']