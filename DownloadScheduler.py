__author__ = 'leonardoalbuquerque'

import atexit
from apscheduler.scheduler import Scheduler
from Main import Main
import thread
import logging

class DownloadScheduler():

    logging.basicConfig()

    def __init__(self, socketio):
        main = Main(socketio)

        cron = Scheduler(daemon=True)
        cron.start()
        #thread.start_new_thread(main.start, ())


        @cron.interval_schedule(seconds=1)
        def job_function():
            # Do your work here
            main.start()

        # Shutdown your cron thread if the web process is stopped
        atexit.register(lambda: cron.shutdown(wait=False))