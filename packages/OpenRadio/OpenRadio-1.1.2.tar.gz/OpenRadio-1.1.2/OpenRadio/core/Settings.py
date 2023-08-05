from toml import dump, load
from .const import LOG_LEVEL, LOG_HANDLER, CONFIG_FILE, CONFIG_DIR
import os
import sys
import logging

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(LOG_HANDLER)


# Simple class for editing ~/.config/OpenRadio/config.toml
class Settings:
    def __init__(self):
        self._load_config()

    def _get_yaml_fd(self, delete: bool = False):
        if not os.path.exists(CONFIG_DIR):
            os.makedirs(CONFIG_DIR)

        if not os.path.exists(CONFIG_FILE) or delete:
            fd = open(CONFIG_FILE, "w+")
        else:
            fd = open(CONFIG_FILE, "r")
        return fd

    def _load_config(self) -> None:
        config_fd = self._get_yaml_fd()

        self.toml = load(config_fd)

        if self.toml == None:
            self.toml = {}
            LOGGER.debug("Empty Toml using empty dict.")

        config_fd.close()

    # Returns config for module by domain
    def get_config(self, domain: str) -> dict:
        keys = self.toml.keys()
        return self.toml.get(domain, {})

    # Save config for module by domain
    def save_config(self, domain: str, data: dict) -> None:
        if not isinstance(data, dict):
            LOGGER.warning("Function returned config not in dict format not saving.")

        self.toml[domain] = data
        config_fd = self._get_yaml_fd(delete=True)
        dump(self.toml, config_fd)
        config_fd.close()
