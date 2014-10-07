from django.conf import settings
from celery.task import PeriodicTask
#from cdr.aggregate import set_concurrentcall_analytic
#from django.core.cache import cache
#from cdr.models import Switch
from common.only_one_task import only_one
from datetime import datetime, timedelta
#import sqlite3
#import asterisk.manager
import traceback


from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

from import_cdr_mongodb import import_cdr_freeswitch_mongodb
from hdmonitor import mail

#Note: if you import a lot of CDRs the first time you can have an issue here
#we need to make sure the user import their CDR before starting Celery
#for now we will increase the lock limit to 1 hours
LOCK_EXPIRE = 60 * 60 * 1  # Lock expires in 1 hours


class sync_cdr_pending(PeriodicTask):
    """
    A periodic task that checks for pending CDR to import
    """
    run_every = timedelta(seconds=10)  # every 10 secs

    @only_one(ikey="sync_cdr_pending", timeout=LOCK_EXPIRE)
    def run(self, **kwargs):
        logger.info('TASK :: sync_cdr_pending')

        # Import from Freeswitch Mongo
        import_cdr_freeswitch_mongodb()

        return True


class hdmonitor(PeriodicTask):
    """
    A periodic task that checks for monitore HD
    """
    run_every = timedelta(minutes=60) 

    @only_one(ikey="hdmonitor")
    def run(self, **kwargs):
        logger.info('TASK :: hdmonitor')
        
	try:
		print 'executing hdmonitor'
		mail() # HD monitor - Mail
		print 'end hdmonitor'
	except Exception,e:
		traceback.print_exc()

        return True


