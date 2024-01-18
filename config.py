from datetime import timedelta
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    DEVELOPMENT = False
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'secret'
    FLASK_SECRET = SECRET_KEY
    JWT_SECRET_KEY = 'b8dad7b10bba86fe6ed93069'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)


class DevConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = "postgres://db_ez1h_user:E3MUwcuyxlK8eioxTwB0GnrW3LGbKRRC@dpg-cmk80qev3ddc738q9tlg-a.frankfurt-postgres.render.com/db_ez1h"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False


config = {
    'dev': DevConfig,
    'test': TestConfig,
    'default': DevConfig,
}
