import random
import string
from itertools import product


def get_word(size):
    return "".join(random.choice(string.ascii_lowercase) for _ in range(size))


def get_words(amount, min_size=4, max_size=10):
    for _ in range(amount):
        yield get_word(random.randrange(min_size, max_size))


def hash1(data):
    return ord(data[0]) + ord(data[1]) if len(data) > 1 else 0


def hash2(data):
    return ord(data[-1]) + ord(data[-2]) if len(data) > 1 else 0


def hash3(data):
    return ord(data[0]) + ord(data[-1]) if len(data) > 1 else 0


def hash4(data):
    return sum(ord(c) for c in data)


def collision_handle(hash_, size):
    j = hash_ % size
    perturb = hash_
    while True:
        yield j % size
        j = (5*j) + 1 + perturb
        perturb >>= 1


class Map(object):

    BASE_SIZE = 10
    MULT = 1.5
    META_KEYS = (M_COLLISIONS, M_CMP) = range(2)

    def __init__(self, hashfunc=hash4, size=BASE_SIZE):
        self.data = [None] * size
        self.cap = size
        self.size = 0
        self.hashfunc = hashfunc
        self.meta = {self.M_COLLISIONS: 0,
                     self.M_CMP: 0}

    def reset_meta(self):
        for key in self.META_KEYS:
            self.meta[key] = 0

    def __contains__(self, key):
        hash_ = self.hashfunc(key) % self.cap
        if self.data[hash_] == key:
            self.meta[self.M_CMP] += 1
            return True
        else:
            for new_hash_ in collision_handle(hash_, self.cap):
                self.meta[self.M_COLLISIONS] += 1
                self.meta[self.M_CMP] += 1
                if not self.data[new_hash_]:
                    return False
                if self.data[new_hash_] == key:
                    return True

    def get_meta(self):
        return self.meta

    def add(self, key):
        hash_ = self.hashfunc(key) % self.cap
        if self.data[hash_] == key:
            self.meta[self.M_CMP] += 1
            return
        elif not self.data[hash_]:
            self.meta[self.M_CMP] += 1
            self.data[hash_] = key
        else:
            for new_hash_ in collision_handle(hash_, self.cap):
                self.meta[self.M_COLLISIONS] += 1
                self.meta[self.M_CMP] += 1
                if not self.data[new_hash_]:
                    self.data[new_hash_] = key
                    break
        self.size += 1
        if self.size > int(self.cap * 0.7):
            self.cap = int(self.cap * self.MULT)
            new_data = [None] * self.cap
            old_data = self.data
            self.data = new_data
            self.size = 0
            for key in old_data:
                if key:
                    self.add(key)

    def remove(self, key):
        hash_ = self.hashfunc(key) % self.cap
        if self.data[hash_] == key:
            self.meta[self.M_CMP] += 1
            self.data[hash_] = None
            self.size -= 1
        else:
            for new_hash_ in collision_handle(hash_, self.cap):
                self.meta[self.M_COLLISIONS] += 1
                self.meta[self.M_CMP] += 1
                if self.data[new_hash_] == key:
                    self.data[new_hash_] = None
                    self.size -= 1
                    return
                if not self.data[new_hash_]:
                    raise Exception("No such element in map!")

    def __str__(self):
        return "[%s]\nfilled: %s capacity: %s" % (", ".join(map(str, filter(None, self.data))), self.size, self.cap)


if __name__ == "__main__":
    HASH_FUNC = (hash1, hash2, hash3, hash4, )
    TESTS = (50, 70, 90, )

    for hashfunc, fillness in product(HASH_FUNC, TESTS):
        print("\n\nhash function: %s, fillness: %s" % (hashfunc.__name__, fillness, ))
        m = Map(hashfunc, 128)
        for word in get_words(fillness):
            m.add(word)
        m.reset_meta()
        print("map size: %s map cap: %s" % (m.size, m.cap, ))
        for word in get_words(20):
            m.add(word)
        print("%s cap." % (m.cap, ))
        print("Collisions: %s Compares: %s" % (m.meta[Map.M_COLLISIONS], m.meta[Map.M_CMP], ))
