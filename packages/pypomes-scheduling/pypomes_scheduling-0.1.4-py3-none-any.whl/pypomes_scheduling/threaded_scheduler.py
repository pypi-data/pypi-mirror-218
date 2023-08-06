from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
import pytz
import threading


class __ThreadedScheduler(threading.Thread):
    """
    A scalable implementation of *APScheduler*'s *BlockingScheduler*, running as single or multiple instances,
    each on its own thread.
    """
    _scheduler: BlockingScheduler
    _logger: logging.Logger
    _stopped: bool

    def __init__(self, timezone: pytz.timezone, retry_interval: int, logger: logging.Logger = None):

        threading.Thread.__init__(self)

        self._stopped = False
        self._logger = logger
        self._scheduler = BlockingScheduler(logging=logger,
                                            timezone=timezone,
                                            jobstore_retry_interval=retry_interval)
        if self._logger is not None:
            self._logger.info("Instanced, with timezone "
                              f"'{timezone}' and retry interval '{retry_interval}'")

    def run(self):
        """
        Start the scheduler in itas own thread.
        """
        # stay in loop until 'stop()' is invoked
        while not self._stopped:
            if self._logger is not None:
                self._logger.info("Started")

            # start the scheduler, blocking until it is interrupted
            self._scheduler.start()

        self._scheduler.shutdown()
        if self._logger is not None:
            self._logger.info("Finished")

    def schedule_job(self, job: callable, job_id: str, job_name: str,
                     cron_expr: str, job_args: tuple = None, start: datetime = None):
        """
        Schedule the given *job*, with the parameters
        :param job: the callable object to be scheduled
        :param job_id: the id of the scheduled job
        :param job_name: the name of the scheduled job
        :param cron_expr: the CRON expression directing the execution times
        :param job_args: the arguments to be passed to the scheduled job
        :param start: the start timestamp for the scheduling process
        :return:
        """
        # approximately, convert symbols to CRON expression
        expr: str
        match cron_expr:
            case "@reboot":
                expr = "1 0 * * *"                      # daily, at 00h01
            case "@midnight":
                expr = "0 0 * * *"                      # daily, at 00h00
            case "@hourly":
                expr = "0 * * * *"                      # every hour, at minute 0 (??h00)
            case "@daily":
                expr = "1 0 * * *"                      # daily, at 00h01
            case "@weekly":
                expr = "0 0 * * 0"                      # on sundays, at 00h00
            case "@monthly":
                expr = "0 0 1 * *"                      # on the first day of the month, at 00h00
            case "@yearly" | "@annually":
                expr = "0 0 1 1 *"                      # on January 1st, at 00h00
            case _:
                expr = cron_expr

        # CRON expression: <minute> <hour> <day-of-month> <month> <day-of-week>
        vals: list[str] = expr.split()
        vals = [None if val == '?' else val for val in vals]
        aps_trigger = CronTrigger(minute=vals[0],
                                  hour=vals[1],
                                  day=vals[2],
                                  month=vals[3],
                                  day_of_week=vals[4],
                                  start_date=start)
        self._scheduler.add_job(func=job,
                                trigger=aps_trigger,
                                args=job_args,
                                id=job_id,
                                name=job_name)
        if self._logger is not None:
            self._logger.info(f"Job '{job_name}' scheduled, with CRON '{cron_expr}'")

    def stop(self):
        """
        Stop the scheduler.
        :return:
        """
        if self._logger is not None:
            self._logger.info("Finishing...")
        self._stopped = True
