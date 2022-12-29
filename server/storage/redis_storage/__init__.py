import asyncio
import aioredis
import json
import asyncio
import logging

from settings import LOG_LEVEL
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)

default_options = {
    "name": "redis",
    "ingress-topics": ["ingress-vcons"],
    "egress-topics":[],
    "redis-set-name": "call_log",
    "redis-list-name": "call_log_list",
}
options = {}

async def start(opts=default_options):
    logger.info("Starting the call_log plugin")

    try:
        r = aioredis.Redis(host='localhost', port=6379, db=0)
        p = r.pubsub(ignore_subscribe_messages=True)
        await p.subscribe(*opts['ingress-topics'])

        while True:
            try:
                message = await p.get_message()
                if message:
                    vConUuid = message['data'].decode('utf-8')
                    logger.info("Redis received vCon: {}".format(vConUuid))
                    # Save this vCon into Redis set.
                    await r.sadd(opts["redis-set-name"], vConUuid)
                    # Save this vCon into Redis list.
                    await r.lpush(opts["redis-list-name"], vConUuid)
                await asyncio.sleep(0.01)

            except Exception as e:
                print("REDIS adapter error: {}".format(e))

    except asyncio.CancelledError:
        logger.debug("Redis storage adapter Cancelled")

    logger.info("Redis storage adapter stopped")    