from loguru import logger

from modules.redis_api import Redis


class APIAuth:
    def __init__(self, clientid: str, username: str, password: str, ipaddr: str) -> None:
        self._clientid = clientid
        self._username = username
        self._password = password
        self._ipaddr = ipaddr

        # self._db = API_DB()  # For User/Pass
        self._redis = Redis()  # For Status TODO: Change for Influx

    async def authentication(self):

        fail_result = await self._redis.check_ban(self._ipaddr)

        if not fail_result:
            return False

        api_key_result = await self._redis.get_api_pair(self._password, self._ipaddr)

        if not api_key_result:

            select_result = self._db.select(key=self._password)

            # Check API Key
            if select_result:
                if select_result['user'] == self._username:
                    await self._redis.set_api_pair(self._password, self._ipaddr)
                    return True

            # Check IP For Ban

            return False

        return True