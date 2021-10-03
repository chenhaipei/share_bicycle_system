from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from .models import *
import datetime
import uuid
import json


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
    finish_time = datetime.datetime.utcnow()
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
    cost = 0.0
    for t in trans:
        cost += t.calculate()
    content = {
        "transactions": trans,
        "cost": round(cost, 3),
        "balance": round((customer.balance - cost), 3)
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
        unique=uuid.uuid4().hex,
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
    lat = request.POST.get("lat", 0.0)
    lng = request.POST.get("lng", 0.0)
    trans = Transaction.objects.get(id=ID)
    trans.status = True
    trans.finish_position_lat = lat
    trans.finish_position_lng = lng
    trans.save()
    bike = trans.bike
    bike.position_lat = lat
    bike.position_lng = lng
    bike.available = True
    bike.save()
    return HttpResponseRedirect("/transactions/")


@login_required
@require_http_methods(['POST'])
def feedback(request, ID):
    bike = Bike.objects.get(id=ID)
    customer = Customer.objects.get(account=request.user)
    record = Record(
        unique=uuid.uuid4().hex,
        bike=bike,
        customer=customer,
        content=request.POST.get('content')
    )
    bike.need_repair = True
    bike.save()
    record.save()
    content = {
        "content": record
    }
    return render(request, "bike/feedback.html", content)


@login_required
@require_http_methods(['POST', 'GET'])
def charge(request):
    if request.method == "GET":
        return render(request, "bike/charge.html", None)
    value = float(request.POST.get('value'))
    customer = Customer.objects.get(account=request.user)
    customer.balance = customer.balance + abs(value)
    customer.save()
    content = {
        "value": abs(value)
    }
    return render(request, "bike/charge.html", content)


@require_http_methods(['POST', 'GET'])
def chart(request):
    finish_time = datetime.datetime.utcnow()
    finish_time = "%04d-%02d-%02dT%02d:%02d:%02d" % (finish_time.year, finish_time.month, finish_time.day, finish_time.hour, finish_time.minute, finish_time.second)
    bikes = Bike.objects.all()
    b, v = list(), list()

    if request.method == "GET":
        content = {"finish_time": finish_time}
        return render(request, "bike/chart.html", content)
    
    start_time = request.POST.get("start_time")
    end_time = request.POST.get("end_time")
    start_time = datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S")
    end_time = datetime.datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S")
    for bike in bikes:
        b.append("Bike #" + bike.unique)
        trans = Transaction.objects.filter(bike=bike, status=True, start_time__gt=start_time, finish_time__lt=end_time)
        v.append(len(trans))
    content = {
        "Bikes": json.dumps(b),
        "Values": json.dumps(v),
        "finish_time": finish_time
    }
    return render(request, "bike/chart.html", content)
