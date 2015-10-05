__author__ = 'leonardoalbuquerque'

import atexit
from apscheduler.scheduler import Scheduler
from Main import Main
import thread

class DownloadScheduler():
    def __init__(self, socketio):
        main = Main(socketio)

        cron = Scheduler(daemon=True)
        # Explicitly kick off the background thread
        cron.start()
        thread.start_new_thread(main.start, ())


        @cron.interval_schedule(hours=2)
        def job_function():
            # Do your work here
            main.start()

        # Shutdown your cron thread if the web process is stopped
        atexit.register(lambda: cron.shutdown(wait=False))