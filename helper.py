import random

from config import CHARACTERISTIC_MAX_INT, CHARACTERISTIC_MIN_INT


def random_int():
    return random.randint(CHARACTERISTIC_MIN_INT, CHARACTERISTIC_MAX_INT)
