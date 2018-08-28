import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') \
                 or 'mLZXlBhl7hoV39xt6PUsJI8N3UUF8r575E77953YH7hIDOv12Yw9kua4nU75xybyyFDfSM6ZO4UPW4UO69e98lisAItyUTkI2TbplZTsDdfdM9ZG'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # 163 mail config
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.163.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '465'))
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
    # ['true', 'on', '1']
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'true')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME','huang_9119596')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD','gb231212')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <huang_9119596@163.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN','huang_9119596@163.com')
    # Bootstrap flask config
    BOOTSTRAP_USE_MINIFIED = True
    BOOTSTRAP_SERVE_LOCAL = True
    BOOTSTRAP_CDN_FORCE_SSL = True
    FLASKY_POSTS_PER_PAGE = 10
    # file upload path and file upload extensions
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'app/static/uploads')
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') \
                              or 'mysql://MaterialDBA:pdf-lib.org&huang_huang118@database.pdflibr.com:3306/Material_Development?charset=utf8'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') \
                              or 'mysql://MaterialDBA:pdf-lib.org&huang_huang118@database.pdflibr.com:3306/Material_Test?charset=utf8'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get( 'PRODUCTION_DATABASE_URL') \
                              or 'mysql://MaterialDBA:pdf-lib.org&huang_huang118@database.pdflibr.com:3306/Material_Production?charset=utf8'


config = {
    'developemnt': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
