import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    REDIS_HOST = "redis"
    REDIS_PORT = 6379

