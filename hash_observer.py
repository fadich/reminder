import os
import re
import time
import hashlib

from typing import Iterable, Callable


class HashObserver(object):

    def __init__(self, path: str = '.', exclude: Iterable = None):
        self.path = path
        self.excluded = set(exclude or ('.idea', 'venv', '.git'))

    def filter_excluded(self, names: Iterable) -> Iterable:
        def regex_excluded(item):
            for exclude in self.excluded:
                if '*' in exclude and re.match(exclude.replace('*', '(.*)'), item):
                    return True
            return False

        res = []
        for name in names:
            if name in self.excluded or regex_excluded(name):
                continue
            res.append(name)

        return res

    def walk(self, abspath: str):
        if not os.path.isdir(abspath):
            return [abspath, ]

        res = []
        items = self.filter_excluded(os.listdir(abspath))
        for item in items:
            res.extend(self.walk(os.path.join(abspath, item)))

        return res

    @property
    def hash(self):
        path_hash = hashlib.md5()
        for filepath in self.walk(os.path.abspath(self.path)):
            try:
                with open(filepath, 'rb') as file:
                    filehash = hashlib.md5(file.read()).hexdigest()
                    path_hash.update(filehash.encode())
            except Exception as e:
                print(f'Error {e}')

        return path_hash.hexdigest()

    def observe(self, callback: Callable, *args, **kwargs):
        hsh = self.hash
        while True:
            time.sleep(0.1)
            if self.hash == hsh:
                continue
            hsh = self.hash
            callback(*args, **kwargs)
