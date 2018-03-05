import pickle

import redis
from enum import Enum

from ..app.config import Config
from ..amazon_extractor import get_amazon_data_from_id

r = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0, decode_responses=True)

DETAILS_ID = ":details"
FEATURES_ID = ":features"
N_ARTICLES = 6


class Cat(Enum):
    __order__ = "TECH HOME HIFI PHOTO INNOV"
    TECH = "tech"
    HOME = "home"
    HIFI = "hifi"
    PHOTO = "photo"
    INNOV = "innov"

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


class Category:
    def __init__(self, category, list_of_article=None):

        category = Cat(category)

        if list_of_article is None:
            self.articles = {k: v
                             for k, v
                             in {f"{category}:article{index}": retrieve_item(f"{category}:article{index}")
                                 for index
                                 in range(1, N_ARTICLES + 1)}.items()
                             if v}
        else:
            self.articles = {f"{category}:{key}": save_item(f"{category}:{key}", value)
                             for key, value
                             in list_of_article.items() if value}


def save_item(key, _id):
    data = get_amazon_data_from_id(_id)
    data["_id"] = _id
    # if data.get("features"):
    #     print(data.get("features"))
    #     hset_key(key + FEATURES_ID, data.get("features"))
    #     data.pop("features")
    #
    if data.get("details"):
         hset_key(key + DETAILS_ID, data.get("details"))
         data.pop("details")

    return hset_key(key, data)


def retrieve_item(key):
    data = hget_key(key=key)
    data["details"] = hget_key(key + DETAILS_ID)
    return {k: v for k, v in data.items() if v}


def hset_key(key, value):
    r.hmset(key, value)
    return value


def hget_key(key):
    res = r.hgetall(key)
    return res


def remove_key(key):
    return r.delete(key)
