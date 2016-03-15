from django.shortcuts import render, redirect
from news_check.models import Company, Vibe
# from news_check.api_get import update_company
from news_check.api_get_v2 import *
from django.utils.timezone import utc
import datetime


# Create your views here.
def index(request):
    return render(
        request,
        'index.html'
    )


# Create your views here.
def companies(request):
    companies = Company.objects.all()
    return render(
        request,
        'company/companies.html',
        {'companies': companies}
    )


def company_detail(request, symbol=None):
    # if redirected
    # if "symbol" in request.session:
    #     symbol = request.session.get("symbol")
    company = Company.objects.get(symbol=symbol)
    try:
        vibe = Vibe.objects.filter(company=company).latest('updated_at')
        context = {
            'company': company,
            'vibe': vibe
        }
    except:
        context = {'company': company}
    return render(
        request,
        'company/detail.html',
        context
    )


def update_vibe(request, symbol):
    # add messages to display about updated or not
    time_diff = 216000
    company = Company.objects.get(symbol=symbol)
    # check if vibe has ever been calculated
    if Vibe.objects.filter(company=company).exists():
        # if other vibes exist, check how recently
        vibe = Vibe.objects.filter(company=company).latest('updated_at')
        # if it's been a while
        if get_time_diff(vibe.updated_at) > time_diff:
            try:
                # try to get new data
                RunData(source="pip", company=company.full_name, save=True).run()
            # ideally catch exception and try api method
            except Exception as e:
                # if error, print it
                print(e)
    else:
        # try to get new data
        check = RunData(source="pip", company=company.full_name, save=True).run()
        print("pip not working in view")
        # ideally catch exception and try api method
        if check is False:
            check = RunData(source="api", company=company.full_name, save=True).run()
            print("api not working in view")
        if check is False:
            print("api and pip both failed for " + company.full_name)

    return redirect("company:detail", symbol=symbol)


def get_time_diff(time):
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    timediff = now - time
    return timediff.total_seconds()
