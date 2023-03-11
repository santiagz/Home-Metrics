import influxdb_client
from influxdb_client.rest import ApiException
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync
from loguru import logger

# Self Import
from data.loader import config


class InfluxDB:
    def __init__(self) -> None:
        self._session = InfluxDBClientAsync(url=config.influx.host, token=config.influx.key, org="STV")

    async def write_temp(self, device, temp, ipaddr):

        async with InfluxDBClientAsync(url=config.influx.host, token=config.influx.key, org="STV") as client:

            write_api = client.write_api()

            rec = influxdb_client.Point(device).tag("ipaddress", ipaddr).field("temperature", float(temp))

            try:

                await write_api.write(bucket="evian", org="STV", record=rec)

            except ApiException as e:
                logger.error(f"InfluxDB Error.")

            await client.close()

    async def write_humid(self, device, humid, ipaddr):

        async with InfluxDBClientAsync(url=config.influx.host, token=config.influx.key, org="STV") as client:

            write_api = client.write_api()

            rec = influxdb_client.Point(device).tag("ipaddress", ipaddr).field("humidity", float(humid))

            try:

                await write_api.write(bucket="evian", org="STV", record=rec)

            except ApiException as e:
                logger.error(f"InfluxDB Error.")

            await client.close()

