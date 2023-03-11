from loguru import logger

from modules.db import API_DB
from modules.redis_api import Redis


class APIACL:
    def __init__(self, access: str, username: str, clientid: str, ipaddr: str, topic: str) -> None:
        self._access = access
        self._username = username
        self._clientid = clientid
        self._ipaddr = ipaddr
        self._topic = topic

        self._db = API_DB()
        self._redis = Redis()

    async def access_control(self):
        select_result = self._db.select(user=self._username)

        # TODO: Make ACL For Access Type
        # logger.debug(f"{self._access}")

        root_path = self._topic.split('/')[0]

        if root_path in select_result['access']:
            return True

        # TODO: Make Fail to Ban with REDIS

        await self._redis.add_ban(self._ipaddr)

        return False

