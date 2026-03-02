from apscheduler.schedulers.background import BackgroundScheduler
from commit import perform_commits
import time

#
if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    # Initialize the rest of the application here, or before the scheduler initialization
    scheduler.add_job(perform_commits, 'interval', minutes = 60)  # Run every hour
    #scheduler.add_listener(listener)
    scheduler.start()
    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()