import os, locale, pytz
from dotenv import load_dotenv

load_dotenv()


class Config:

    locale.setlocale(locale.LC_TIME, "id_ID.UTF-8")

    ROOT_DIR = os.path.dirname(__file__)

    SECRET_KEY = "987587809909090hjnjkmk"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URI = f"postgresql+psycopg2://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_TEST_NAME')}"


config = {"development": DevelopmentConfig, "testing": TestingConfig}
