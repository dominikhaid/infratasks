# Desc: Runs once on startup to execute local operation before connection to hosts is made
from pyinfra import logger, config

config.REQUIRE_PACKAGES = "../requirements.txt"
logger.info('Executing local operations')
