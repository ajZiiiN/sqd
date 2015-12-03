__author__ = 'ajeetjha'

import logging


logger = logging.getLogger("RunnerLog")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("/Users/ajeetjha/zi/sqd/logs/runner.log")
handler.setFormatter(formatter)
logger.addHandler(handler)