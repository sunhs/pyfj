import os
import pickle
import click
from pyfj import jumper


# fj -l | awk '{if (NF==3) {print $2} else if (NF==4) {prinnt $3}}'
@click.command()
@click.argument("old_db")
def migrate(old_db: str):
    with open(old_db) as f:
        paths = [path.strip() for path in f.readlines()]
        paths = [path for path in paths if path]

    j = jumper.Jumper()

    new_db = []
    if os.path.exists(j.db_path):
        with open(j.db_path, "rb") as f:
            new_db = pickle.load(f)

    new_db += paths
    new_db = new_db[: j.conf.nhistory]
    with open(j.db_path, "wb") as f:
        pickle.dump(new_db, f)


if __name__ == "__main__":
    migrate()
