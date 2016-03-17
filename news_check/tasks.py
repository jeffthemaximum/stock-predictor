from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from news_check.api_get_v2 import RunData
from news_check.models import Vibe, Company

logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="update_vibe",
    ignore_result=True
)
def task_save_latest_vibe():
    """
    updates vibe for every company
    """
    # get last company
    last_company = Company.objects.latest('id')
    # get last company id
    lid = last_company.id
    # get latest vibe
    vibe = Vibe.objects.latest("updated_at")
    # get company of latest vibe
    company = vibe.company
    # get id of latest company
    cid = company.id
    # check if lid - cid
    if lid == cid:
        company = Company.objects.get(id=1)
    else:
        # get next company
        company = Company.objects.get(id=(cid + 1))
    # run api on that company
    print(company.full_name)

    check = RunData(source="pip", company=company.full_name, save=True).run()
    print("pip not working in view")
    # ideally catch exception and try api method
    if check is False:
        check = RunData(source="api", company=company.full_name, save=True).run()
        print("api not working in view")
    if check is False:
        print("api and pip both failed for " + company.full_name)
