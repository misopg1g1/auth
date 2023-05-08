import os


class AppConfigValues:
    ENCRYPTION_KEY_SECRET = os.getenv("ENCRYPTION_KEY_SECRET", "ASuJ-vtjlvAuUdFDTdeMOHoCTjlS_dipLtp6_7rQ_kw=")
    JWT_SECRET = os.getenv("JWT_SECRET", "secret")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_NAME = os.getenv("DB_NAME", "postgres")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_USERNAME = os.getenv("DB_USERNAME", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
    DB_DIALECT = os.getenv("DB_DIALECT", "postgresql")
    DB_DRIVER = os.getenv("DB_DRIVER", "psycopg2")
    DB_URL = os.getenv("DB_URL",
                       f"{DB_DIALECT}+{DB_DRIVER}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
