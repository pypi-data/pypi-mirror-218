import io
import json
import sys
import os
import serial
import re
import time
import inspect
import logger
import streamer as s
import jobqueue as j
import immediate as i
import device as d
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

logging = logger.Logger()
logging.setLevel(logger.INFO)

class Service:
    device = None
    scheduler = None
    device = None
    root = os.path.dirname(inspect.getfile(lambda: None))

    def __init__(self):
        global scheduler

        scheduler = BackgroundScheduler()
        self.streamer = s.Streamer()
        self.immediate_queue = i.Immediate()
        self.job_queue = j.JobQueue()
        self.device = d.Device()
        process = self.add_job(self.process_job_queue)
        scheduler.start()

        return

    def add_job(self, function):
        return scheduler.add_job(function, 'date', run_date=datetime.now(), max_instances=1)

    def connect(self, device_path):
        self.device.set(device_path)
        logging.info("[ hc ] wake up grbl...")

        self.immediate_queue.clear()

        bline = b'\r\n\r\n'
        self.device.write(bline)
        time.sleep(2)

        line = re.sub('\s|\(.*?\)','',bline.decode()).upper() # Strip comments/spaces/new line and capitalize
        while self.device.inWaiting() > 0:
            response = self.device.readline().strip() # wait for grbl response
            logging.info("[ " + line + " ] " + response.decode())

        self.simple_command(io.BytesIO(b'$$'))
        self.simple_command(io.BytesIO(b'$I'))
        self.simple_command(io.BytesIO(b'$G'))

        return

    # We cleanup the queues and disconnect by issuing an immediate shut down function execution.
    def disconnect(self):
        self.device.abort()
        self.immediate_queue.abort()
        self.job_queue.clear()

        def shutdown():
            self.device.close()
            sys.exit(0)

        job = self.add_job(lambda: shutdown())
        return

    def reset(self):
        bline = b'\x18'
        self.device.write(bline)
        time.sleep(2)

        line = re.sub('\s|\(.*?\)','',bline.decode()).upper() # Strip comments/spaces/new line and capitalize
        while self.device.inWaiting() > 0:
            response = self.device.readline().strip() # wait for grbl response
            logging.info("[ " + line + " ] " + response.decode())

        self.streamer.terminate = True
        self.immediate_queue.terminate = True

        return

    def status(self):
        self.immediate_queue.put(io.BytesIO(b'?'))
        return

    def home(self):
        self.immediate_queue.put(io.BytesIO(b'$H'))
        return

    def unlock(self):
        self.immediate_queue.put(io.BytesIO(b'$X'))
        return

    def stop(self):
        self.immediate_queue.put(io.BytesIO(b'!'))
        return

    def resume(self):
        self.immediate_queue.put(io.BytesIO(b'~'))
        return

    def jobs(self):
        result = {}
        jobs = list(self.job_queue.queue.queue)
        for i, job in enumerate(jobs, start=1):
            result[str(i)] = job[0]

        return result

    def simple_command(self, inputstream):
        self.immediate_queue.put(io.BytesIO(inputstream.getvalue()))
        return

    # send a streaming job to the queue
    def stream(self, inputstream, jobname):
        streamcopy = io.BytesIO(inputstream.getvalue())
        inputstream.close()

        job = self.job_queue.put([jobname, lambda: self.streamer.stream(streamcopy)])
        logging.info("[ hc ] queued jobs " + str(self.job_queue.qsize()) + ". " + jobname)
        return

    # we process immediate commands first and then queued jobs in sequence
    def process_job_queue(self):
        with self.streamer.lock:
            while True:
                while not self.streamer.is_running and not self.immediate_queue.empty():
                    self.immediate_queue.process_immediate()
                if not self.streamer.is_running and not self.job_queue.empty():
                    queuedjob = self.job_queue.get()
                    jobname = queuedjob[0]
                    lambdajob = queuedjob[1]
                    job = self.add_job(lambdajob)
                    logging.info("[ hc ] queued jobs " + str(self.job_queue.qsize()) + ". streaming " + jobname )

                time.sleep(1)
