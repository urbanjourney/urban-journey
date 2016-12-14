"""
This module is used to configure the loggers used throughout urban_journey.
"""

import logging.config
import yaml
from os.path import dirname, join, isfile

# Load default logging configuration
path = join(dirname(__file__), "default_logging_config.yaml")
with open(path) as f:
    default_config = yaml.load(f)
logging.config.dictConfig(default_config)

# Load a logging configuration file in the current working directory.
path = join("./logging_config.yaml")
if isfile(path):
    with open(path) as f:
        cwd_config = yaml.load(f)
    logging.config.dictConfig(cwd_config)
