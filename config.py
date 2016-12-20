import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '{B&GoKU1Ga0RSY/H-<iyU^m(RlU<>.UR(<SK=Vm'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SUBJECT_PREFIX = '[Rosetta]'
    MAIL_SENDER = 'Rosetta GUI <rosetta.gui@gmail.com>'
    ROSETTA_ADMIN = os.environ.get('ROSETTA_ADMIN')
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'app/static/uploads')
    PHOTO_ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG =  True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'mysql+pymysql://root:phpmysql@localhost/rosetta_sip_gen'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'the.domain.email@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'th3d0m@!n3m@!l121#'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'mysql+pymysql://root:phpmysql@localhost/rosetta_sip_gen_test'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'mysql+pymysql://root:phpmysql@localhost/rosetta_sip_gen_prod'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}