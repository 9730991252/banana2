from django import template
from owner.models import *
from django.db.models import Avg, Sum, Min, Max
from math import *
import math
from datetime import date
from django.utils.safestring import mark_safe
register = template.Library()

@register.filter(is_safe=True)
@register.simple_tag()
def bill_amount_detail(bill_id):
    if bill_id:
        bank = bill_company_paid_amount_bank(bill_id)
        phonepe = bill_company_paid_amount_phonepe(bill_id)
        cash = bill_company_paid_amount_cash(bill_id)
        
        if bank != 0 and phonepe != 0 and cash != 0:
            details = f"Bank { bank }, Phonepe {phonepe}, Cash {cash}"
        
        elif bank != 0 and phonepe != 0:
            details = f"Bank { bank }, Phonepe {phonepe}"
            
        elif bank != 0 :
            details = f"Bank { bank }"
            
            
        elif phonepe != 0 and cash != 0:
            details = f"Phonepe {phonepe}, Cash {cash}"
            
        elif bank != 0 and cash != 0:
            details = f"Bank { bank }, Cash {cash}"
            
        elif phonepe != 0:
            details = f"Phonepe {phonepe}"
        elif cash != 0:
            details = f"Cash {cash}"
        else:
            details = " 0  "

        return mark_safe(details)
    return ""

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
def bill_company_paid_amount_bank(bill_id):
    if bill_id:
        b = Company_bank_transition.objects.filter(company_bill_id=bill_id).aggregate(Sum('amount'))
        bank = b['amount__sum']
        return bank if bank else 0

@register.simple_tag()
def bill_company_paid_amount_phonepe(bill_id):
    if bill_id:
        p = Company_Phonepe_transition.objects.filter(company_bill_id=bill_id).aggregate(Sum('amount'))
        phonepe = p['amount__sum']
        return phonepe if phonepe else 0

@register.simple_tag()
def bill_company_paid_amount_cash(bill_id):
    if bill_id:
        c = Company_cash_transition.objects.filter(company_bill_id=bill_id).aggregate(Sum('amount'))
        cash = c['amount__sum']
        return cash if cash else 0

@register.simple_tag()
def bill_company_paid_amount(bill_id):
    if bill_id:
        total_paid_amount = 0
        
        c = Company_cash_transition.objects.filter(company_bill_id=bill_id).aggregate(Sum('amount'))
        cash = c['amount__sum']
        if cash:
            total_paid_amount += cash
        
        p = Company_Phonepe_transition.objects.filter(company_bill_id=bill_id).aggregate(Sum('amount'))
        phonepe = p['amount__sum']
        if phonepe:
            total_paid_amount += phonepe
        
        b = Company_bank_transition.objects.filter(company_bill_id=bill_id).aggregate(Sum('amount'))
        bank = b['amount__sum']
        if bank:
            total_paid_amount += bank
        
        return total_paid_amount

@register.simple_tag()
def bill_company_pending_amount(bill_id):
    if bill_id:
        total_pending_amount = ''
        
        bill = Company_bill.objects.filter(id=bill_id).aggregate(Sum('total_amount'))
        total_pending_amount = bill['total_amount__sum']
        
        c = Company_cash_transition.objects.filter(company_bill_id=bill_id).aggregate(Sum('amount'))
        cash = c['amount__sum']
        if cash:
            total_pending_amount -= cash
        
        p = Company_Phonepe_transition.objects.filter(company_bill_id=bill_id).aggregate(Sum('amount'))
        phonepe = p['amount__sum']
        if phonepe:
            total_pending_amount -= phonepe
        
        b = Company_bank_transition.objects.filter(company_bill_id=bill_id).aggregate(Sum('amount'))
        bank = b['amount__sum']
        if bank:
            total_pending_amount -= bank
        
        if total_pending_amount is None:
            return 0
        else:
            return total_pending_amount

@register.simple_tag()
def user_pending_bill_amount(user_id):
    if user_id:
        total_pending_amount = ''
        
        bill = Farmer_bill.objects.filter(office_employee_id=user_id).aggregate(Sum('total_amount'))
        total_pending_amount = bill['total_amount__sum']
        
        c = Farmer_cash_transition.objects.filter(office_employee_id=user_id).aggregate(Sum('amount'))
        cash = c['amount__sum']
        if cash:
            total_pending_amount -= cash
        
        p = Farmer_Phonepe_transition.objects.filter(office_employee_id=user_id).aggregate(Sum('amount'))
        phonepe = p['amount__sum']
        if phonepe:
            total_pending_amount -= phonepe
        
        b = Farmer_bank_transition.objects.filter(office_employee_id=user_id).aggregate(Sum('amount'))
        bank = b['amount__sum']
        if bank:
            total_pending_amount -= bank
        
        if total_pending_amount == None:
            return 0
        else:
            return total_pending_amount
        
@register.simple_tag()
def company_pendding_bill_amount(company_id):
    if company_id:
        total_pending_amount = ''
        
        bill = Company_bill.objects.filter(company_id=company_id).aggregate(Sum('total_amount'))
        total_pending_amount = bill['total_amount__sum']
        
        c = Company_cash_transition.objects.filter(company_bill__company_id=company_id).aggregate(Sum('amount'))
        cash = c['amount__sum']
        if cash:
            total_pending_amount -= cash
        
        p = Company_Phonepe_transition.objects.filter(company_bill__company_id=company_id).aggregate(Sum('amount'))
        phonepe = p['amount__sum']
        if phonepe:
            total_pending_amount -= phonepe
        
        b = Company_bank_transition.objects.filter(company_bill__company_id=company_id).aggregate(Sum('amount'))
        bank = b['amount__sum']
        if bank:
            total_pending_amount -= bank
        
        if total_pending_amount == None:
            return 0
        else:
            return total_pending_amount
        
@register.simple_tag()
def product_cost_net_weight(weight, empty_box):
    a = (weight - empty_box)
    return a

@register.simple_tag()
def stalk_net_weight(wasteage, weight, empty_box):
    a = (((int(wasteage) + int(weight) - int(empty_box)) / 100) * 8)
    return math.floor(a)


        
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
    total = 0
    pending_amount_total = 0
    completed_amount_total = 0
    farmer_pendding_bill = []
    farmer_completed_bill = []
    if farmer_id:
        bill = Farmer_bill.objects.filter(farmer_id=farmer_id)
        pending_bill = Farmer_bill.objects.filter(farmer_id=farmer_id, paid_status=0)
        for b in pending_bill:
            pending_amount = b.total_amount
            c = Farmer_cash_transition.objects.filter(farmer_bill_id=b.id).aggregate(Sum('amount'))
            cash = c['amount__sum']
            if cash:
                pending_amount -= cash
            
            p = Farmer_Phonepe_transition.objects.filter(farmer_bill_id=b.id).aggregate(Sum('amount'))
            phonepe = p['amount__sum']
            if phonepe:
                pending_amount -= phonepe
            
            bank = Farmer_bank_transition.objects.filter(farmer_bill_id=b.id).aggregate(Sum('amount'))
            bank = bank['amount__sum']
            if bank:
                pending_amount -= bank
            
            if pending_amount == None:
                return 0
            
            pending_amount_total += pending_amount
            farmer_pendding_bill.append({'id':b.id, 'bill_number':b.bill_number, 'pending_amount':pending_amount})
        #?//?//?//?//?//?
        completed_bill = Farmer_bill.objects.filter(farmer_id=farmer_id, paid_status=1)
        for b in completed_bill:
            completed_amount_total += b.total_amount
            farmer_completed_bill.append({'id':b.id, 'bill_number':b.bill_number, 'amount':b.total_amount})

            
        if bill:
            total = bill.aggregate(Sum('total_amount'))
            total = total['total_amount__sum']
            if total is None:
                total = 0
    return{
        'total':total,
        'farmer_pendding_bill':farmer_pendding_bill,
        'pending_amount_total':pending_amount_total,
        'farmer_completed_bill':farmer_completed_bill,
        'completed_amount_total':completed_amount_total
    }
