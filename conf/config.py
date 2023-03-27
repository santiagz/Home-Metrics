from dataclasses import dataclass
from environs import Env


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
        self.env = Env()
        self.env.read_env('../.env')

    @property
    def config(self):
        return Config(
            redis=RedisConfig(
                host=self.env.str('REDIS_HOST'),
                port=self.env.int('REDIS_PORT'),
                passwd=self.env.str('REDIS_PASS')
            ),
            influx=InfluxConfig(
                host=self.env.str('INFLX_HOST'),
                key=self.env.str('INFLX_KEY')
            ),
            db=Database(
                host=self.env.str('DB_HOST'),
                port=self.env.str('DB_PORT'),
                user=self.env.str('DB_USER'),
                passwd=self.env.str('DB_PASS'),
                database=self.env.str('DB_DATABASE')
            )
        )


config = LoadConfig().config
