from django.shortcuts import render, redirect
from news_check.models import Company, Vibe
from news_check.api_get import update_company
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
    try:
        vibe = Vibe.objects.filter(company=company).latest('updated_at')
        if get_time_diff(vibe.updated_at) > time_diff:
            update_company(company.full_name)
    except:
        update_company(company.full_name)
    # set session so that you can get company symbol back out in detail
    request.session["symbol"] = company.symbol
    return redirect("company:detail", symbol=symbol)


def get_time_diff(time):
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    timediff = now - time
    return timediff.total_seconds()
