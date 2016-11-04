#by ganben, to demo hbmqtt sub
import logging
import asyncio

from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1, QOS_2

logger = logging.getLogger(__name__)

SERVER = 'mqtt://47.88.15.107/'
TOPIC1 = '$SYS/broker/uptime'
TOPIC2 = '$SYS/broker/load/#'
TOPIC3 = 'demo'

@asyncio.coroutine
def uptime_coro():
    C = MQTTClient()
    yield from C.connect(SERVER)

    yield from C.subscribe([
        (TOPIC1, QOS_1),
        (TOPIC3, QOS_2),
        ])
    logger.info("------Subscribed----")
    try:
        for i in range(1, 100):
            message = yield from C.deliver_message()
            packet = message.publish_packet
            print("%d: %s => %s" % (i, packet.variable_header.topic_name,
                str(packet.payload.data)))
        yield from C.unsubscribe([TOPIC1,
                TOPIC3])
        logger.info("----UnSubscribed-----")
        yield from C.disconnect()
    except ClientException as ce:
        logger.error("Client exception: %s" % ce )


if __name__ == '__main__':
    formatter = "[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    asyncio.get_event_loop().run_until_complete(uptime_coro())

