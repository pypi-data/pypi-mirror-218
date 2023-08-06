import io
from pathlib import Path
from typing import List, Set

import requests
import zipfile

from cobra.utils.caches import MODULE_DB_CACHE
from cobra.utils.configurations import COBRA_VERSION
from cobra.utils import logging
from cobra.utils.urls import MODULE_DB_URL


def get_module_db(name: str, version: str = COBRA_VERSION, force_download: bool = False) -> Path:
    """
    Returns module database from CoBRA if it exists.

    :param name: Name of module database to look for.
    :param version: Version of CoBRA to find this module database for.
    :param force_download: If True, module database will be downloaded even if it exists in cache.
    :return: Path to module database file.
    :raises FileNotFoundError: If module database does not exist in CoBRA of specific version.
    """
    module_db_dir = MODULE_DB_CACHE.joinpath(version).joinpath(name)
    module_db_file = module_db_dir.joinpath('modules.json')
    if not force_download and module_db_file.exists():
        return module_db_file
    module_db_uri = f"{MODULE_DB_URL}/{name}?zip=True"
    logging.debug(f"Trying to get {module_db_uri}")
    r = requests.get(module_db_uri)
    logging.debug(f"Request status: {r.status_code}")
    if r.status_code == 200:
        module_db_dir.mkdir(parents=True, exist_ok=True)
        zipfile.ZipFile(io.BytesIO(r.content)).extractall(module_db_dir)
        return module_db_file
    else:
        raise FileNotFoundError(f"Asset {name} (version {version}) does not exist in CoBRA.")


def get_available_module_dbs(version: str = COBRA_VERSION, locally: bool = False) -> Set[str]:
    """
    Returns a set of module databases available in CoBRA of specific version.

    :param version: Version of CoBRA to find module databases for.
    :param locally: If True, will return module databases available in cache.
    :return: Set of module databases available in CoBRA of specific version.
    :raises ValueError: If module databases could not be retrieved from CoBRA.
    """
    if locally:
        return {x.name for x in MODULE_DB_CACHE.joinpath(version).iterdir()}
    else:
        r = requests.get(MODULE_DB_URL)
        if r.status_code == 200:
            return set(r.json())
        else:
            raise ValueError(f"Could not get available module databases from CoBRA (error {r.status_code}).")


def get_schema(version: str = COBRA_VERSION) -> Path:
    """
    Get schema of the CoBRA module database.

    :param version: Version of CoBRA to find schema for.
    :return: Path to schema file.
    :raise ValueError: If schema does not found for specific CoBRA version or other backend error encountered.
    """
    raise NotImplementedError


def get_urdf(module_db, module_order: List[str], version: str = COBRA_VERSION) -> Path:
    """
    Get URDF of robot with specific module order. The assets are stored alongside the URDF.

    :param module_db: Name of module database to use.
    :param module_order: List of modules in order from base to end-effector.
    :param version: Version of CoBRA to find module database for.
    :return: Path to URDF file.
    :raise ValueError: If module database does not exist in CoBRA of specific version or other backend error.
    """
    raise NotImplementedError
