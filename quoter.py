import asyncio

from requests_html import HTMLSession
import atparts

from redis import Redis
from rq import Queue
from rq.job import Job

# Setup RQ with REdis
redis_conn = Redis('localhost', 6379)
quoter_queue = Queue('quoter', connection=resid_conn)

class Quoter:

    def __init__(self):
        self.start_session()
        self.loggedin = False
    
    def start_session(self):
        self.session = HTMLSession()
        self.active = True
    
    def close_session(self):
        self.session.close()
        self.active = False
    
    async def part(self, pn: str):
        info = quoter_queue.enqueue(atparts.get_part(self.session, pn, self.loggedin, verbose=True))
        job = Job.fetch(info.id, connection=redis_conn)
        while job.get_status != 'finished':
            if job.get_status == 'failed':
                return None
            job = Job.fetch(info.id, connection=redis_conn)
        info = job.result

        if info:
            info = info._asdict()
            info['vendor'] = 'Air Tractor'
        else:
            info = {
                'pn': pn,
                'desc': 'Not Found'
            }
        return info
