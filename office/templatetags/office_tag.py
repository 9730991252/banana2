from django import template
from owner.models import *
from django.db.models import Avg, Sum, Min, Max
from math import *
import math
from datetime import date
from django.utils.safestring import mark_safe
register = template.Library()



@register.inclusion_tag('inclusion_tag/office/company_details.html')
def company_details(company_id):
    if company_id:
        company = Company.objects.get(id=company_id)
        bills = Company_bill.objects.filter(company_id=company_id)
        return {
            'company': company,
            'bill':bills
        }
    return {}
        

@register.simple_tag()
def product_cost_net_weight(weight, empty_box):
    a = (weight - empty_box)
    return a
 
@register.simple_tag()
def user_pending_bill_amount(office_employee_id):
    amount = Farmer_bill.objects.filter(office_employee_id=office_employee_id).aggregate(Sum('total_amount'))['total_amount__sum']
    if amount == None:
        amount = 0
    recived_amount = Farmer_payment_transaction.objects.filter(office_employee_id=office_employee_id).aggregate(Sum('amount'))['amount__sum']
    if recived_amount == None:
        recived_amount = 0
    amount -= int(recived_amount)
    if int(amount) < 0:
        amount = 0
    return amount

@register.simple_tag()
def company_pendding_bill_amount (company_id):
    amount = Company_bill.objects.filter(company_id=company_id).aggregate(Sum('total_amount'))['total_amount__sum']
    if amount == None:
        amount = 0
    
    recived_amount = company_recived_payment_transaction.objects.filter(company_id=company_id).aggregate(Sum('amount'))['amount__sum']
    if recived_amount == None:
        recived_amount = 0
    amount -= int(recived_amount)
    if int(amount) < 0:
        amount = 0
    return amount
        
        
@register.simple_tag()
def stalk_net_weight(wasteage, weight, empty_box):
    a = (((int(wasteage) + int(weight) - int(empty_box)) / 100) * 8)
    return math.floor(a)


@register.inclusion_tag('inclusion_tag/office/company_transaction.html')
def company_transaction(company_id):
    return {
        'transaction':company_recived_payment_transaction.objects.filter(company_id=company_id).order_by('-date'),
        'total_amount':company_recived_payment_transaction.objects.filter(company_id=company_id).aggregate(Sum('amount'))['amount__sum']
    }
        
@register.inclusion_tag('inclusion_tag/office/pendding_completed_farmer_bill.html')
def pendding_completed_farmer_bill(farmer_id):
    if farmer_id:
        farmer_bill = Farmer_bill.objects.filter(farmer_id=farmer_id)
        total_amount = farmer_bill.aggregate(Sum('total_amount'))
        total_amount = total_amount['total_amount__sum']
        print(total_amount)
        
@register.inclusion_tag('inclusion_tag/office/user_pendding_all_amount.html')
def user_pendding_all_amount(shope_id):
    return{
        'all_users':office_employee.objects.filter(shope_id=shope_id)
    }
    
@register.inclusion_tag('inclusion_tag/office/company_pendding_all_amount.html')
def company_pendding_all_amount(shope_id):
    return{
        'company':Company.objects.filter(shope_id=shope_id)
    }

@register.inclusion_tag('inclusion_tag/office/farmer_bill_detail.html')
def farmer_bill_detail(farmer_id):
    completed_amount_total = Farmer_payment_transaction.objects.filter(farmer_id=farmer_id).aggregate(Sum('amount'))['amount__sum']
    if completed_amount_total == None:
        completed_amount_total = 0
    total = Farmer_bill.objects.filter(farmer_id=farmer_id).aggregate(Sum('total_amount'))['total_amount__sum']
    if total == None:
        total = 0
    return{
        'total':total,
        'farmer_bill':Farmer_bill.objects.filter(farmer_id=farmer_id),
        'transaction':Farmer_payment_transaction.objects.filter(farmer_id=farmer_id).order_by('date'),
        'completed_amount_total':completed_amount_total,
        'total_amount':(int(total) - int(completed_amount_total))
    }
 