import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') \
                 or ''
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # 163 mail config
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.163.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '465'))
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
    # ['true', 'on', '1']
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'true')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'huang_9119596')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'gb231212')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <huang_9119596@163.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN', 'huang_9119596@163.com')
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




config = {
    'developemnt': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
