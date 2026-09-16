import json
import logging

from typing import Dict

from pathlib import Path

logger = logging.getLogger(__name__)

CONFIG_PATH = Path(__file__).parent / "config.json"

if not CONFIG_PATH.exists():
    with open(CONFIG_PATH, "w") as f:
        json.dump({}, f)


def load() -> Dict[str, str]:
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def add_entry(attr: str, val: str) -> None:
    config = load()
    if config.get(attr) == val:
        return

    config[attr] = val
    with open(CONFIG_PATH, "w") as f:
        logger.info(f"{attr}: {val}")
        json.dump(config, f)


def read_entry(attr: str) -> str:
    config = load()
    if config.get(attr):
        return config[attr]

    logger.exception(f"Configuration file key {attr} not found")
    return None
