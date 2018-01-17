import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or 'mLZXlBhl7hoV39xt6PUsJI8N3UUF8r575E77953YH7hIDOv12Yw9kua4nU75xybyyFDfSM6ZO4UPW4UO69e98lisAItyUTkI2TbplZTsDdfdM9ZG'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SENDER = 'Web Master <huang_9119596@163.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PROT = 465
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEV_DATABASE_URL') or ''


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'TEST_DATABASE_URL') or ''


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'TEST_DATABASE_URL') or ''


config = {
    'developemnt': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
