from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
import datetime
from .models import *


@require_http_methods(['GET'])
def index(request):
    bikes = Bike.objects.all()
    content = {"bikes": bikes}
    return render(request, "bike/index.html", content)


@require_http_methods(['GET', 'POST'])
def logins(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/")
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            content = {'wrong': True}
            return render(request, "bike/login.html", content)
    else:
        return render(request, "bike/login.html", None)


@login_required
@require_http_methods(['GET'])
def logouts(request):
    logout(request)
    return HttpResponseRedirect("/")


@login_required
@require_http_methods(['GET'])
def transaction(request, ID):
    trans = Transaction.objects.get(id=ID)
    finish_time = datetime.datetime.now()
    finish_time = "%04d-%02d-%02dT%02d:%02d:%02d" % (finish_time.year, finish_time.month, finish_time.day, finish_time.hour, finish_time.minute, finish_time.second)
    start_time = "%04d-%02d-%02dT%02d:%02d:%02d" % (trans.start_time.year, trans.start_time.month, trans.start_time.day, trans.start_time.hour, trans.start_time.minute, trans.start_time.second)
    content = {
        'transaction': trans,
        'start_time': start_time,
        'finish_time': finish_time
    }
    return render(request, "bike/transaction.html", content)


@login_required
@require_http_methods(['GET'])
def transactions(request):
    customer = Customer.objects.get(account=request.user)
    trans = Transaction.objects.filter(customer=customer).order_by('-start_time')
    content = {
        "transactions": trans
    }
    return render(request, "bike/transactions.html", content)


@login_required
@require_http_methods(['GET'])
def rent(request, ID):
    bike = Bike.objects.get(id=ID)
    if not bike.available:
        return HttpResponseRedirect("/detail/%d/" % ID)
    customer = Customer.objects.get(account=request.user)
    trans = Transaction(
        customer=customer,
        bike=bike,
        start_position_lat=bike.position_lat,
        start_position_lng=bike.position_lng
    )
    trans.save()
    bike.available = False
    bike.save()
    return HttpResponseRedirect("/transaction/%d/" % trans.id)


@login_required
@require_http_methods(['GET'])
def detail(request, ID):
    bike = Bike.objects.get(id=ID)
    content = {"bike": bike}
    return render(request, "bike/bike.html", content)


@login_required
@require_http_methods(['POST'])
def finish(request, ID):
    finish_time = request.POST.get("finish_time")
    lat = request.POST.get("lat", 0.0)
    lng = request.POST.get("lng", 0.0)
    finish_time = datetime.datetime.strptime(finish_time, '%Y-%m-%dT%H:%M:%S')
    trans = Transaction.objects.get(id=ID)
    trans.status = True
    trans.finish_time = finish_time
    trans.finish_position_lat = lat
    trans.finish_position_lng = lng
    trans.save()
    bike = trans.bike
    bike.available = True
    bike.save()
    return HttpResponseRedirect("/transactions/")


@login_required
@require_http_methods(['POST'])
def feedback(request, ID):
    bike = Bike.objects.get(id=ID)
    customer = Customer.objects.get(account=request.user)
    record = Record(
        bike=bike,
        customer=customer,
        content=request.POST.get('content')
    )
    record.save()
    content = {
        "content": record
    }
    return render(request, "bike/feedback.html", content)
