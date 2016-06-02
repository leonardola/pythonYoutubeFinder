__author__ = 'leonardoalbuquerque'

import atexit
from apscheduler.scheduler import Scheduler
from Main import Main
import thread
import logging

class DownloadScheduler():

    logging.basicConfig()

    def __init__(self, socketio):
        self.main = Main(socketio)

        self.execute_now()

        cron = Scheduler(daemon=True)
        cron.start()

        @cron.interval_schedule(hours=1)
        def job_function():
            # Do your work here
            self.main.start()

        # Shutdown your cron thread if the web process is stopped
        atexit.register(lambda: cron.shutdown(wait=False))

    def execute_now(self):
        thread.start_new_thread(self.main.start, ())

