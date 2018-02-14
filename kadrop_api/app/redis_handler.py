import redis
from enum import Enum

r = redis.StrictRedis(host="redis", port=6379, db=0)

N_ARTICLES = 6


class Cat(Enum):
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
                             in { f"{category}:article{index}": get_key(f"{category}:article{index}")
                                 for index
                                 in range(1, N_ARTICLES+1)}.items()
                             if v}
        else:
            self.articles = {f"{category}:{key}": set_key(f"{category}:{key}", value)
                             for key, value
                             in list_of_article.items() if value}

        print(self.articles)


def set_key(key, value):
    r.set(key, value=value)
    return value


def get_key(key):
    res = r.get(key)
    return res.decode() if res else None


def remove_key(key):
    return r.delete(key)


if __name__ == "__main__":
    cate = Category(category=Cat.TECH)