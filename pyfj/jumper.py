from typing import *
import dataclasses
import json
import os
import pickle

from pyfj import search


@dataclasses.dataclass
class Config:
    nhistory: int = 200
    nhint: int = 10
    # sep: str = "/|_|-"
    sep: str = "/"

    def load_config(self, path: str):
        if not os.path.exists(path):
            return

        data: Dict[str, Union[str, int]] = json.load(path)
        for k, v in data.items():
            if k in self.__annotations__:
                v = self.__annotations__[k](v)
                self.__setattr__(k, v)

    def save_config(self, path: str):
        json.dump(self.__dict__, path, indent=4)


@dataclasses.dataclass
class Jumper:
    db_path: str = dataclasses.field(init=False)
    db: List[str] = dataclasses.field(init=False)
    conf: Config = dataclasses.field(init=False)
    dir: str = os.path.expanduser(os.path.join("~", ".pyfj"))

    def __post_init__(self):
        if not os.path.isdir(self.dir):
            os.makedirs(self.dir)

        self.db_path = os.path.join(self.dir, "db")
        self._load_db()
        self.conf = Config()
        self.conf.load_config(os.path.join(self.dir, "config.json"))

    def _load_db(self):
        if not os.path.exists(self.db_path):
            self.db = []
            return

        with open(self.db_path, "rb") as f:
            self.db = pickle.load(f)

    def _update_db(self, path: str, idx: Optional[int] = None):
        if idx is not None:
            self.db.pop(idx)
        self.db.insert(0, path)
        self.db = self.db[: self.conf.nhistory]

        with open(self.db_path, "wb") as f:
            pickle.dump(self.db, f)

    def jump(self, patterns: List[str]) -> Optional[str]:
        if not patterns:
            patterns = [os.path.expanduser("~")]

        if len(patterns) == 1 and os.path.isdir(patterns[0]):
            path = os.path.abspath(os.path.expanduser(patterns[0]))
            idx = None
            try:
                idx = self.db.index(path)
            except ValueError:
                ...
            self._update_db(path, idx)
            return path

        rst = search.match_dispatcher(patterns, self.db, sep=self.conf.sep)

        if not rst:
            return None

        idx, matched = rst[0]
        self._update_db(matched, idx)
        return matched

    def hint(self, patterns: List[str]) -> List[str]:
        rst = search.match_dispatcher(patterns, self.db, self.conf.nhint, self.conf.sep)
        return [tpl[1] for tpl in rst]
