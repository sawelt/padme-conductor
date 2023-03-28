from collections import defaultdict
from pathlib import Path
from typing import Dict, List

from padme_conductor.Query import Query

_WORK_DIR_NAME = "/padme-conductor"
_SAVE_DIR_NAME = "save"
_SAVE_METADATA_FILE_NAME = ".save_metadata.json"
_SAVE_METADATA_DEFAULT = {"runs": 0, "visited_stations": []}
_STATION_ID = "STATION_ID"
_station_queries: Dict[str, List[Query]] = defaultdict(list)
_work_dir: Path = Path(_WORK_DIR_NAME)
_save_dir: Path = Path(_WORK_DIR_NAME) / _SAVE_DIR_NAME
_save_metadata_path = _save_dir / _SAVE_METADATA_FILE_NAME
