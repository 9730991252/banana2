from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import *
from owner.models import *
from django.db.models import Q
from datetime import date
import datetime
# Create your views here.
def farmer_check(request):
    if request.method == 'GET':
        c = ''
        name = request.GET['name']
        address = request.GET['address']
        mobile = request.GET['mobile']
        shope_id = request.GET['shope_id']
        if 1 < len(name) :
            c = Farmer.objects.filter(Q(name__icontains=name),shope_id=shope_id)
        if 1 < len(address) :
            c = Farmer.objects.filter(Q(address__icontains=address),shope_id=shope_id)
        if 1 < len(mobile) :
            c = Farmer.objects.filter(Q(mobile__icontains=mobile),shope_id=shope_id)
        context={
            'c':c[0:3]
        }
        t = render_to_string('ajax/office/farmer_check.html', context)
    return JsonResponse({'t': t})

def select_bill(request):
    if request.method == 'GET':
        f = ''
        bill_id = request.GET['bill_id']
        bill = Farmer_bill.objects.filter(id=bill_id).first()
        context={
            'bill':bill
        }
        t = render_to_string('ajax/office/select_bill.html', context)
    return JsonResponse({'t': t})

def save_company(request):
    if request.method == 'GET':
        name = request.GET['name'].upper()
        shope_id = request.GET['shope_id']
        
        c_id = ''
        if name:
            if Company.objects.filter(name = name, shope_id=shope_id).exists():
                c = Company.objects.filter(shope_id=shope_id,name=name).last()
                c_id = c.id
            else:
                Company(
                    shope_id=shope_id,
                    name=name
                ).save()
                c = Company.objects.filter(shope_id=shope_id,name=name).last()
                c_id = c.id
    return JsonResponse({'id': c_id})

def check_company(request):
    if request.method == 'GET':
        c = ''
        name = request.GET['name'].upper()
        shope_id = request.GET['shope_id']
        if name != '':
            c = Company.objects.filter(Q(name__icontains=name),shope_id=shope_id)
        if c:
            status = 1
        else:
            status = 0
        context={
            'c':c[0:3]
        }
        t = render_to_string('ajax/office/check_company.html', context)
    return JsonResponse({'t': t,'status':status})

def select_company(request):
    if request.method == 'GET':
        c = ''
        c_id = request.GET['id']
        c = Company.objects.filter(id=c_id).first()
        context={
            'c':c,
            'today_date':date.today()
        }
        t = render_to_string('ajax/office/select_company.html', context)
    return JsonResponse({'t': t})

def search_company(request):
    if request.method == 'GET':
        c = ''
        words = request.GET['words']
        shope_id = request.GET['shope_id']
        if words:
            print('words:',words)
            c = Company.objects.filter( Q(name__icontains=words), shope_id=shope_id)
        context={
            'c':c[0:3]
        }
        t = render_to_string('ajax/office/search_company.html', context)
    return JsonResponse({'t': t})


def save_date_company_bill(request):
    if request.method == 'GET':
        bill_id = request.GET['bill_id']
        date = request.GET['date']
        Company_bill.objects.filter(id=bill_id).update(id=bill_id,date=date)
    return JsonResponse({'status': 1})

def save_date_farmer_bill(request):
    if request.method == 'GET':
        bill_id = request.GET['bill_id']
        date = request.GET['date']
        Farmer_bill.objects.filter(id=bill_id).update(id=bill_id,date=date)
    return JsonResponse({'status': 1})