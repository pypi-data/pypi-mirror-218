import io
import re
import serial
import logger
import threading
import queue as q
import device as d
import time

logging = logger.Logger()
logging.setLevel(logger.INFO)


# Singleton Immediate
class Immediate:
    instance = None
    is_running = False
    lock = None
    immediate_queue = None
    immediate = None
    paused = None
    nudge_count = None
    nudge_logged = None
    start_time = None
    device = None

    def __new__(self):
        if self.instance is None:

            self.instance = super().__new__(self)
            self.lock = threading.Lock()
            self.immediate_queue = q.Queue()
            self.immediate = True
            self.paused = False
            self.nudge_count = 0
            self.nudge_logged = False
            self.device = d.Device()

        return self.instance

    # we put an immediate command to be handled immediately (i.e. particularly for hold, resume and status (!, ~, ?))
    # this is intended to help avoid disrupting the serial buffer and flow of the gcode stream
    def put(self, inputstream):
        self.immediate_queue.put(inputstream.getvalue())
        return

    def process_immediate(self):
        try:
            while not self.immediate_queue.empty() or self.paused:
                if not self.immediate_queue.empty():
                    ins = io.BytesIO(self.immediate_queue.get())
                    sl = ins.getvalue().decode().strip()

                    bline = b''
                    if sl == '?' or sl == '!' or sl == '?':
                        bline = str.encode(sl).upper()
                    else:
                        bline = str.encode(sl + "\n").upper()

                    self.device.write(bline)

                    line = bline.decode().strip()

                    if line == '!':
                        logging.info("[ " + line + " ] " + "ok")
                        self.paused = True
                    elif line == '$X' and self.paused:
                        logging.info("[ hc " + line + " ] " + "not during feed hold")
                    elif line == '$$' and self.paused:
                        logging.info("[ hc " + line + " ] " + "not during feed hold")
                    elif line == '?':
                        response = self.device.readline().strip()
                        logging.info("[ " + line + " ] " + response.decode())
                    else:
                        self.start_time = time.monotonic()  # Get the current time at the start to evaluate stalling and nudging
                        while self.device.inWaiting() == 0:
                            self.stalled()
                            time.sleep(1)

                        while self.device.inWaiting() > 0:
                            response = self.device.readline().strip() # wait for grbl response
                            if self.nudge_count > 0:
                                logging.info("[ " + line + " ] " + response.decode())
                                self.nudge_logged = True
                                self.nudge_count = 0
                            elif not self.nudge_logged:
                                logging.info("[ " + line + " ] " + response.decode())

                            if response.find(b'error') >= 0:
                                logging.info("[ hc ] gcode error " + response.decode())
                                raise Exception("[ hc ] gcode error " + response.decode())

                            time.sleep(1/100)
                        self.nudge_logged = False

                    if line == '~':
                        self.paused = False

                time.sleep(1/100)

        except Exception as exception:
            self.immediate_queue.queue.clear()

        finally:
            self.paused = False
            self.immediate = False
            self.paused = False
            self.nudge_logged = False
            self.nudge_count = 0

        return

    # If we've been stalled for more than some amount of time, we nudge the GRBL controller with an empty byte array
    # We reset the timer after nudging to avoid excessive nudging for long operations.
    def stalled(self):
        current_time = time.monotonic()
        elapsed_time = current_time - self.start_time
        logging.debug(elapsed_time)

        if elapsed_time >= 1:
            self.start_time = time.monotonic()
            self.nudge_count += 1
            logging.info("[ hc ] nudge " + str(self.nudge_count))
            self.device.write(b'\n')    
