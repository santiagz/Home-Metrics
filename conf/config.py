from dataclasses import dataclass
# from data.vault import ENV  # TODO: Change for Redis or smth else


@dataclass
class RedisConfig:
    host: str
    port: int
    passwd: str


@dataclass
class Database:
    host: str
    port: str
    user: str
    passwd: str
    database: str


@dataclass
class InfluxConfig:
    host: str
    key: str


@dataclass
class Config:
    redis: RedisConfig
    influx: InfluxConfig
    db: Database


class LoadConfig(object):
    def __init__(self):
        self.env = ENV.get_secrets()

    @property
    def config(self):
        return Config(
            redis=RedisConfig(
                host=self.env['redis_host'],
                port=self.env['redis_port'],
                passwd=self.env['redis_pass']
            ),
            influx=InfluxConfig(
                host=self.env['inflx_host'],
                key=self.env['inflx_key']
            ),
            db=Database(
                host=self.env['db_api_host'],
                port=self.env['db_api_port'],
                user=self.env['db_api_user'],
                passwd=self.env['db_api_pass'],
                database=self.env['db_api_database']
            )
        )
