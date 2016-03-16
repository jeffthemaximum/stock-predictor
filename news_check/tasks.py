from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from news_check.api_get_v2 import RunData

logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="update_vibe",
    ignore_result=True
)
def task_save_latest_flickr_image():
    """
    updates vibe for every company
    """
    # TODO change to loop across all companies
    # try to get new data
    check = RunData(source="pip", company="Sysco", save=True).run()
    print("pip not working in view")
    # ideally catch exception and try api method
    if check is False:
        check = RunData(source="api", company="Sysco", save=True).run()
        print("api not working in view")
    if check is False:
        print("api and pip both failed for " + "Sysco")