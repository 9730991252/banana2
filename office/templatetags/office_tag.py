from django import template
from owner.models import *
from django.db.models import Avg, Sum, Min, Max
from math import *
import math
from datetime import date
from django.utils.safestring import mark_safe
from office.views import *
register = template.Library()



@register.inclusion_tag('inclusion_tag/office/company_details.html')
def company_details(company_id):
    if company_id:
        company = Company.objects.get(id=company_id)
        bills = Company_bill.objects.filter(company_id=company_id)
        bill_amount = bills.aggregate(Sum('total_amount'))['total_amount__sum']
        if bill_amount == None:
            bill_amount = 0
        transactions_t =  company_recived_payment_transaction.objects.filter(company_id=company_id).aggregate(Sum('amount'))['amount__sum']
        if transactions_t == None:
            transactions_t = 0
            
            
        paid_bill_amount = Company_bill.objects.filter(company_id=company_id, paid_status = 1).aggregate(Sum('total_amount'))['total_amount__sum']
        if paid_bill_amount == None:
            paid_bill_amount = 0
            
        remening_amount = (int(transactions_t) - int(paid_bill_amount))
        
        bill = Company_bill.objects.filter(company_id=company_id, paid_status=0).order_by('date')
        
        bill_id = 0
        for b in bill:
            if remening_amount >= b.total_amount:
                remening_amount -= b.total_amount
            else:
                bill_id = b.id
                if int(remening_amount) != 0:
                    remening_amount = int(b.total_amount) - int(remening_amount)
                break 
        r = {'bill_id':bill_id, 'remening_amount':remening_amount}
        return {
            'company': company,
            'bill':bills,
            'transactions': company_recived_payment_transaction.objects.filter(company_id=company_id),
            'transactions_t':transactions_t,
            'bill_amount':bill_amount,
            'bill_amount_total':bill_amount,
            'final_amount':(int(bill_amount) - int(transactions_t)),
            'remening_amount':r
        }
    return {}

@register.inclusion_tag('inclusion_tag/office/farmer_details.html')
def farmer_details(farmer_id):
    if farmer_id:
        farmer = Farmer.objects.get(id=farmer_id)
        bills = Farmer_bill.objects.filter(farmer_id=farmer_id)
        bill_amount = bills.aggregate(Sum('total_amount'))['total_amount__sum']
        if bill_amount == None:
            bill_amount = 0
        transactions_t =  Farmer_payment_transaction.objects.filter(farmer_id=farmer_id).aggregate(Sum('amount'))['amount__sum']
        if transactions_t == None:
            transactions_t = 0
            
        # remening_amount = change_farmer_bill_paid_status(farmer_id)
        

        recived_payment = Farmer_payment_transaction.objects.filter(farmer_id=farmer_id).aggregate(Sum('amount'))['amount__sum']
        if recived_payment == None:
            recived_payment = 0
        paid_bill_amount = Farmer_bill.objects.filter(farmer_id=farmer_id, paid_status = 1).aggregate(Sum('total_amount'))['total_amount__sum']
        if paid_bill_amount == None:
            paid_bill_amount = 0
        remening_amount = (int(recived_payment) - int(paid_bill_amount))
        bill = Farmer_bill.objects.filter(farmer_id=farmer_id, paid_status=0).order_by('date')
        
        bill_id = 0
        for b in bill:
            if remening_amount >= b.total_amount:
                b.paid_status = 1
                b.save()
                remening_amount -= b.total_amount
            else:
                bill_id = b.id
                if int(remening_amount) != 0:
                    remening_amount = int(b.total_amount) - int(remening_amount)
                break
        remening_amount = {'bill_id':bill_id, 'remening_amount':remening_amount}

        ########################        
        return {
            'farmer': farmer,
            'bill':bills,
            'transactions': Farmer_payment_transaction.objects.filter(farmer=farmer),
            'transactions_t':transactions_t,
            'bill_amount':bill_amount,
            'bill_amount_total':bill_amount,
            'final_amount':(int(bill_amount) - int(transactions_t)),
            'remening_amount':remening_amount
        }
    return {}
         
@register.inclusion_tag('inclusion_tag/office/company_details_unpaid_bills.html')
def company_details_unpaid_bills(company_id):
    if company_id:
        company = Company.objects.get(id=company_id)
        bills = Company_bill.objects.filter(company_id=company_id, paid_status=0).order_by('-date')
        bill_amount = Company_bill.objects.filter(company_id=company_id).aggregate(Sum('total_amount'))['total_amount__sum']
        if bill_amount == None:
            bill_amount = 0
        transactions_t =  company_recived_payment_transaction.objects.filter(company_id=company_id).aggregate(Sum('amount'))['amount__sum']
        if transactions_t == None:
            transactions_t = 0
            
        ###################
        paid_bill_amount = Company_bill.objects.filter(company_id=company_id, paid_status = 1).aggregate(Sum('total_amount'))['total_amount__sum']
        if paid_bill_amount == None:
            paid_bill_amount = 0
            
        remening_amount = (int(transactions_t) - int(paid_bill_amount))
        
        bill = Company_bill.objects.filter(company_id=company_id, paid_status=0).order_by('date')
        
        bill_id = 0
        for b in bill:
            if remening_amount >= b.total_amount:
                remening_amount -= b.total_amount
            else:
                bill_id = b.id
                if int(remening_amount) != 0:
                    remening_amount = int(b.total_amount) - int(remening_amount)
                break 
        r = {'bill_id':bill_id, 'remening_amount':remening_amount}
        #################


        return {
            'company': company,
            'bill':bills,
            'transactions': company_recived_payment_transaction.objects.filter(company_id=company_id),
            'transactions_t':transactions_t,
            'bill_amount':Company_bill.objects.filter(company_id=company_id).aggregate(Sum('total_amount'))['total_amount__sum'],
            'bill_amount_total':Company_bill.objects.filter(company_id=company_id, paid_status=0).aggregate(Sum('total_amount'))['total_amount__sum'],
            'final_amount':(int(bill_amount) - int(transactions_t)),
            'remening_amount':r
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
        'total_amount':company_recived_payment_transaction.objects.filter(company_id=company_id).aggregate(Sum('amount'))['amount__sum'],
        'today_date':date.today(),
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
 