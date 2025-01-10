from django.shortcuts import render, redirect
from sunil.models import *
from owner.models import *
from django.views.decorators.csrf import csrf_exempt
import math
from num2words import num2words
from django.db.models import Avg, Sum, Min, Max
from django.contrib import messages 
import time
# Create your views here.
def download_all_company_report(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile).first()
        context={
            'e':e,
            'bill':Company_bill.objects.filter(shope_id=e.shope_id),

        }
        return render(request, 'report/download_all_company_report.html', context)
    else:
        return redirect('login')