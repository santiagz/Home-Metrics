import base64
from loguru import logger
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# CUSTOM IMPORT
from modules.api_methods.auth import APIAuth
from modules.api_methods.acl import APIACL
from modules.influx_api import InfluxDB
from modules.redis_api import Redis
from data.loader import config


app = FastAPI()
influx = InfluxDB()
redis = Redis()


class Auth(BaseModel):
    clientid: str
    username: str
    password: str
    ipaddr: str


class Superuser(BaseModel):
    clientid: str
    username: str


class ACL(BaseModel):
    access: str
    username: str
    clientid: str
    ipaddr: str
    topic: str


# Routes
'''
/mqtt/auth
/mqtt/superuser
/mqtt/acl
'''


@app.get("/")
async def test():
    """ Test Endpoint """

    return {"OK": "OK"}


@app.post("/mqtt/auth")
async def auth(data: Auth):
    """ Authentication

    {
        clientid = "%c",
        username = "%u",
        password = "%P"
    }

    :param data: Dataclass [Auth], incoming data for
    :return: JSONResponse(200, 401)
    """

    ath = APIAuth(clientid=data.clientid, username=data.username, password=data.password, ipaddr=data.ipaddr)

    if await ath.authentication():
        return JSONResponse(status_code=200, content={})

    return JSONResponse(status_code=401, content={"message": "Unauthirized"})


@app.post("/mqtt/superuser")
async def superuser(data: Superuser):
    """ SuperUser Ident

    {
        clientid = "%c",
        username = "%u",
        password = "%P"
    }

    :param data: Dataclass [Superuser], incoming data for
    :return: JSONResponse(200, 401)
    """
    return JSONResponse(status_code=401, content={"message": "Unauthirized"})


@app.post("/mqtt/acl")
async def acl(data: ACL):
    """ Access-Control list

    {
        access = "%A",
        username = "%u",
        clientid = "%c",
        ipaddr = "%a",
        topic = "%t"
    }

    :data: Dataclass [Superuser], for ACL
    :return: JSONResponse(200, 401)
    """

    acl_result = APIACL(access=data.access, username=data.username,
                        clientid=data.clientid, ipaddr=data.ipaddr, topic=data.topic)

    if await acl_result.access_control():
        return JSONResponse(status_code=200, content={})

    return JSONResponse(status_code=401, content={"message": "Unauthirized"})


@app.post("/mqtt/webhook")
async def webhook(request: Request):
    """ Webhook Incoming

    :request: Incoming JSON Request
    :return: JSONResponse(200, 401)
    """
    data = {
        'action': 'message_publish', 'dup': False, 'from_clientid': 'hm-134', 'from_ipaddress': '172.21.0.3:44889',
        'from_node': 1, 'from_username': 'device_1', 'packet_id': None, 'payload': 'bWVzc2FnZXM6IDA=',
        'qos': 0, 'retain': False, 'topic': 'hm/test-device/door1', 'ts': 1676377545238
    }

    incoming_data = await request.json()

    # logger.debug(incoming_data)

    match incoming_data['action']:
        case "message_publish":
            device = incoming_data['from_clientid']
            endpoint = incoming_data['topic'].split('/')[-1]
            ipaddr = incoming_data['from_ipaddress'].split(':')[0]
            sensor_data = base64.b64decode(incoming_data['payload']).decode('utf-8')
            topic = incoming_data['topic'].split('/')[-1]
            endpoint = 'sensor' if "sensor" in topic else topic

            match endpoint:
                case 'sensor':
                    await redis.set_sensor_status(device, topic, sensor_data)

                case 'temp':
                    await influx.write_temp(device, sensor_data, ipaddr)

                case 'humid':
                    await influx.write_humid(device, sensor_data, ipaddr)

                case _:
                    pass

        case "client_connected":

            await redis.set_device_status(incoming_data['clientid'], 'online')

        case "client_disconnected":

            await redis.set_device_status(incoming_data['clientid'], 'offline')

        case _:
            logger.debug(f'Unknown :action: -> {incoming_data["action"]}')

    return {}
