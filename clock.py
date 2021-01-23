from datetime import datetime
from api import check_if_recent_game
from apscheduler.schedulers.blocking import BlockingScheduler

check_if_recent_game()

sched = BlockingScheduler()

# Schedule job_function to be called every 3 hours
sched.add_job(check_if_recent_game, 'interval', minutes=10)

sched.start()