from scout import db_handler
import os
import concurrent.futures

# celery worker -A cel -c 1

import redis
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']

redis_url = os.getenv('REDISTOGO_URL', 'redis://redistogo:137dd33f39a1fd083ea34578f5984441@spinyfin.redistogo.com:9852/')

conn = redis.from_url(redis_url)


def start_worker():
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()
    return None


if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
        future_to_url = [
                            executor.submit(start_worker), 
                            executor.submit(start_worker), 
                            executor.submit(start_worker), 
                            executor.submit(start_worker), 
                            executor.submit(start_worker), 
                            executor.submit(start_worker), 
                            executor.submit(start_worker), 
                            executor.submit(start_worker), 
                        ]
        print(future_to_url)   
    # with Connection(conn):
    #     worker = Worker(map(Queue, listen))
    #     worker.work()

