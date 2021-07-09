from os import getenv as env

POSTGRES_HOST = env("POSTGRES_HOST", "localhost")
POSTGRES_USER = env("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = env("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = env("POSTGRES_DB", "postgres")
