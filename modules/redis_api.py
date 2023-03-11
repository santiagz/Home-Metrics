import redis
from loguru import logger

from data.loader import config
from modules.db import API_DB


class Redis:
    def __init__(self):
        self._session = redis.Redis(host=config.redis.host, port=config.redis.port, password=config.redis.passwd, db=0)
        self._api = API_DB()

    async def get_api_pair(self, api_key: str, ipaddr: str):

        redis_result = self._session.get(api_key)

        if redis_result:
            if redis_result.decode('utf-8') == ipaddr:
                return True

        return False

    async def set_api_pair(self, api_key: str, ipaddr: str):

        self._session.set(api_key, ipaddr)

    async def check_ban(self, ipaddr: str):

        fail_count = self._session.get(ipaddr)

        if fail_count:
            return False if int(fail_count.decode('utf-8')) >= 5 else True

        return True

    async def add_ban(self, ipaddr: str):

        fail_count = self._session.get(ipaddr)

        if fail_count:

            fail_count = int(fail_count.decode('utf-8'))

            fail_count += 1

            self._session.set(ipaddr, fail_count)

        else:
            self._session.set(ipaddr, 1)

    async def flush_redis(self):
        self._session.flushall()

    async def get_device_status(self, device: str):

        device_status = self._session.get(device)

        if device_status:

            return device_status.decode('utf-8')
        else:
            return False

    async def set_device_status(self, device: str, status: str):

        self._session.set(device, status)

    async def set_sensor_status(self, device: str, sensor: str, status: str):
        device_sensor = device + " " + sensor
        logger.debug(f"{device_sensor} -> {status}")
        self._session.set(device_sensor, status)
