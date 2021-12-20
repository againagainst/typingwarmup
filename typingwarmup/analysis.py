import shelve
from datetime import datetime
from pathlib import Path
from typing import Dict, cast

import disk
from dataholders.dbrecord import DbRecord
from stats import Stats


def persist(excercise: Path, stats: Stats) -> None:
    record = DbRecord(
        excercise.name,
        stats.exercise_length,
        stats.symbols_typed,
        stats.score(),
        stats.mistakes,
    )
    timestamp = datetime.now().strftime(r"%Y-%m-%dT%H:%M:%S")
    with shelve.open(disk.db_filename()) as db:
        db[timestamp] = record


def load() -> Dict[str, DbRecord]:
    result = {}
    with shelve.open(disk.db_filename()) as db:
        for timestamp, record in db.items():
            result[timestamp] = cast(DbRecord, record)
    return result
