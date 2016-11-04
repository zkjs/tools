#-*- encoding=utf-8 -*-
#p3 code for hbmqtt client
#by ganben

import logging
import asyncio

from hbmqtt.client import MQTTClient, ConnectException
from hbmqtt.mqtt.constants import *

logger = logging.getLogger(__name__)

SERVER = 'mqtt://47.88.15.107'
TOPIC3 = 'demo'


config = {
        'will': {
            'topic': TOPIC3,
            'message': b'Dead or alive',
            'qos': 0x01,
            'retain': True
        }
}

@asyncio.coroutine
def test_coro():
    C = MQTTClient()
    yield from C.connect(SERVER)
    tasks = [
            asyncio.ensure_future(C.publish(TOPIC3, b'TEST MESSAGE WITH QOS_0')),
            asyncio.ensure_future(C.publish(TOPIC3, b'TEST MESSAGE WITH QOS_1', qos=QOS_1)),
            asyncio.ensure_future(C.publish(TOPIC3, b'TEST message with qos_2', qos=QOS_2)),
            ]
    yield from asyncio.wait(tasks)
    logger.info("message published")
    yield from C.disconnect

@asyncio.coroutine
def test_coro2():
    try:
        C = MQTTClient()
        ret = yield from C.connect('mqtt://test.mosquitto.org/')
        message = yield from C.publish(TOPIC3, b'TEST MESSAGE WITH QOS_0', qos=0x00)
        message = yield from C.publish(TOPIC3, b'TEST MESSAGE WITH QOS_1', qos=0x01)
        message = yield from C.publish(TOPIC3, b'TEST MESSAGE WITH QOS_2', qos=0x02)
        #print(message)
        logger.info("messages published")
        yield from C.disconnect()
    except ConnectException as ce:
        logger.error("Connection failed: %s" % ce)
        asyncio.get_event_loop().stop()


if __name__ == '__main__':
    formatter = "[%(asctime)s] %(name)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    formatter = "%(message)s"
    logging.basicConfig(level=logging.DEBUG, format=formatter)
    asyncio.get_event_loop().run_until_complete(test_coro())
    asyncio.get_event_loop().run_until_complete(test_coro2())

