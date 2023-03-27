from conf.config import config
from loguru import logger

logger.debug(f'{config.db.user}')
