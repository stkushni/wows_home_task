"""Initialize the SQLite database inside the container."""
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import ORIGINAL_DATABASE
from db.create_db import create_database
from db.populate_db import populate_database


def main() -> None:
    db_path = Path(ORIGINAL_DATABASE)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    create_database(str(db_path))
    populate_database(str(db_path))


if __name__ == "__main__":
    main()
