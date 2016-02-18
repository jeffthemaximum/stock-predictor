from django.shortcuts import render
from news_check.models import Stock

# Create your views here.
def index(request):
    return render(
        request, 
        'index.html'
    )

# Create your views here.
def stocks(request):
    stocks = Stock.objects.all()
    return render(
        request, 
        'stocks.html',
        {'stocks': stocks}
    )

def stock_detail(request, symbol):
    stock = Stock.objects.get(symbol=symbol)
    return render(
        request,
        'stocks/stock_detail.html',
        {'stock': stock}
    )