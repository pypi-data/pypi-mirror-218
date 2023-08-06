"""This module provides the RP To-Do database functionality."""
# rptodo/database.py

import configparser
import json
import dataclasses
from pathlib import Path
from typing import Any, Dict, List, NamedTuple
from ...error import DB_WRITE_ERROR, SUCCESS
from ...extlib.TyperExt.TyperExt import TyperExt
from ...extlib.MgmtExt.log import get_logger

DEFAULT_DB_FILE_PATH = Path.home().joinpath(".cpc_cli.json")


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


class DBResponse(NamedTuple):
    todo_list: List[Dict[str, Any]]
    error: int


class DatabaseHandler:
    def __init__(self, db_path: Path = DEFAULT_DB_FILE_PATH) -> None:
        self._db_path = db_path
        self._logger = get_logger("DM")

    def init_database(self):
        """Create the to-do database."""
        empty_data = {}
        with self._db_path.open("w") as db:
            db.write(json.dumps(empty_data))  # Empty to-do list

    def check_exist_or_create(self, obj, key, content):
        if key not in obj:
            obj[key] = content
        return obj

    def read_matter_cluster(self, group, cluster):
        profile = {}
        try:
            with self._db_path.open("r") as db:
                profile = json.load(db)
        except FileNotFoundError:
            self.init_database()
        self.check_exist_or_create(profile, group, {})
        self.check_exist_or_create(profile[group], cluster, [])
        return profile

    def read_matter_config_cluster(self):
        profile = {}
        try:
            with self._db_path.open("r") as db:
                profile = json.load(db)
        except FileNotFoundError:
            self.init_database()
        group = "matter"
        cluster = "config"
        content = {"max_nodeid": 0, "max_groupid": 0}
        self.check_exist_or_create(profile, group, {})
        self.check_exist_or_create(profile[group], cluster, content)
        return profile

    def read_single_matter_cluster(self, group, cluster, key, target_name):
        target_node = {}
        profile = self.read_matter_cluster(group, cluster)
        for node in profile[group][cluster]:
            if not node[key] == target_name:
                continue
            target_node = node
            break
        return target_node

    def read_match_matter_cluster(self, group, cluster, key, target_name):
        target_list = []
        profile = self.read_matter_cluster(group, cluster)
        for node in profile[group][cluster]:
            if not node[key] == target_name:
                continue
            target_list.append(node)
            break
        return target_list

    def write_matter_profile(self, group, cluster, data) -> DBResponse:
        profile = self.read_matter_cluster(group, cluster)
        self._logger.debug(json.dumps((group, cluster)))
        self._logger.debug(json.dumps(dataclasses.asdict(data)))
        if (dataclasses.asdict(data) not in profile[group][cluster]):
            profile[group][cluster].append(dataclasses.asdict(data))
            with self._db_path.open("w") as db:
                db.write(json.dumps(profile))
        return DBResponse(profile, SUCCESS)

    def modify_matter_profile(self, group, cluster, key, data) -> DBResponse:
        profile = self.read_matter_cluster(group, cluster)
        data = dataclasses.asdict(data)
        self._logger.debug(json.dumps((group, cluster)))
        self._logger.debug(json.dumps(data))
        for idx in range(0, len(profile[group][cluster])):
            if (profile[group][cluster][idx][key] == data[key]):
                profile[group][cluster][idx] = data
                with self._db_path.open("w") as db:
                    db.write(json.dumps(profile))
                return DBResponse(profile, SUCCESS)
        return DBResponse(profile, DB_WRITE_ERROR)

    def modify_matter_profile_with_muiti(self, group, cluster, keys, data) -> DBResponse:
        profile = self.read_matter_cluster(group, cluster)
        data = dataclasses.asdict(data)
        self._logger.debug(json.dumps((group, cluster)))
        self._logger.debug(json.dumps(data))
        for idx in range(0, len(profile[group][cluster])):
            match_counter = 0
            for key, val in keys.items():
                if (str(profile[group][cluster][idx][key]) == str(val)):
                    match_counter += 1
                    if (match_counter == len(keys)):
                        profile[group][cluster][idx] = data
                        with self._db_path.open("w") as db:
                            db.write(json.dumps(profile))
                        return DBResponse(profile, SUCCESS)
        return DBResponse(profile, DB_WRITE_ERROR)

    def update_matter_profile(self, group, cluster, data) -> DBResponse:
        profile = self.read_matter_cluster(group, cluster)
        profile[group][cluster] = data
        with self._db_path.open("w") as db:
            db.write(json.dumps(profile))
        return DBResponse(profile, SUCCESS)

    def write_matter_config_profile(self, config):
        profile = self.read_matter_config_cluster()
        profile['matter']['config'] = config
        with self._db_path.open("w") as db:
            db.write(json.dumps(profile))
        return DBResponse(profile, SUCCESS)
