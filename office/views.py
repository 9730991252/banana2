from django.shortcuts import render, redirect
from sunil.models import *
from owner.models import *
from django.views.decorators.csrf import csrf_exempt
import math
from num2words import num2words
from django.db.models import Avg, Sum, Min, Max
from django.contrib import messages 
import time
import datetime
from datetime import date
from .templatetags.office_tag import *
# Create your views here.

def office_home(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile).first()
        context={
            'e':e,
            'bill':Farmer_bill.objects.filter(id=31).first(),
            'all_users':office_employee.objects.filter(shope_id=e.shope.id)

        }
        return render(request, 'office/office_home.html', context)
    else:
        return redirect('login')
    
def softwar_charges(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile).first()
        context={
            'e':e,
            'payment':Shope_payment.objects.filter(shope_id=e.shope.id).order_by('-id') 
        }
        return render(request, 'office/softwar_charges.html', context)
    else:
        return redirect('login')
    
    
def money(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile).first()
        context={
            'e':e,
            'bill':Farmer_bill.objects.filter(id=31).first(),
            'all_users':office_employee.objects.filter(shope_id=e.shope.id),
            'company':Company.objects.filter(shope_id=e.shope_id)
        }
        return render(request, 'office/money.html', context)
    else:
        return redirect('login')
    

@csrf_exempt
def money_company_details(request,id): 
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile).first()
        if e:
            remening_amount = change_company_bill_paid_status(id)
            
            bill_amount = Company_bill.objects.filter(company_id=id).aggregate(Sum('total_amount'))['total_amount__sum']
            if bill_amount == None:
                bill_amount = 0
            
            recived_amount = company_recived_payment_transaction.objects.filter(shope_id=e.shope_id, company_id=id).aggregate(Sum('amount'))['amount__sum']
            if recived_amount == None:
                recived_amount = 0
                
            b_opn = Company_opning_balance.objects.filter(company_id=id).first()
            
            final_amount = int(bill_amount) - int(recived_amount)
            if b_opn:
                if b_opn.type == 0:
                    final_amount += int(b_opn.balance)
                else:
                    final_amount -= int(b_opn.balance)
            
            if 'edit_opning_balance'in request.POST:
                t = request.POST.get('type')
                amount = request.POST.get('amount')
                
                if Company_opning_balance.objects.filter(company_id=id).exists():
                    of = Company_opning_balance.objects.filter(company_id=id).first()
                    nf = Company_opning_balance.objects.filter(company_id=id).first()
                    nf.balance = amount
                    nf.type = t
                    nf.save() 
                    
                if int(t) == 1:
                    ba = int(math.floor(float(of.balance))) - int(math.floor(float(nf.balance)))
                    bill = Company_bill.objects.filter(company_id=id, paid_status=1).order_by('id')
                    for b in bill:
                        if ba <= b.total_amount:
                            b.paid_status = 0
                            b.save()
                            ba -= b.total_amount
                        else:
                            break
                else:
                    ba = int(math.floor(float(of.balance))) - int(math.floor(float(nf.balance)))
                    bill = Company_bill.objects.filter(company_id=id, paid_status=1).order_by('id')
                    for b in bill:
                        if ba <= b.total_amount:
                            b.paid_status = 0
                            b.save()
                            ba -= b.total_amount
                        else:
                            break
                return redirect('money_company_details', id=id)
            
            if 'add_opning_amount'in request.POST:
                t = request.POST.get('type')
                amount = request.POST.get('amount')
                print(amount)
                if Company_opning_balance.objects.filter(company_id=id).exists():
                    pass
                else:
                    Company_opning_balance(
                        company_id = id,
                        shope_id = e.shope_id,
                        balance = amount,
                        type = t,
                    ).save()
                return redirect('money_company_details', id=id)
            
            if 'cash'in request.POST:
                amount = request.POST.get('cash_amount')
                da = request.POST.get('date')
                if da and amount :
                    save_cash_company_amount(da, amount, e.shope_id, e.id,id)
                else:
                    messages.warning(request,"please insert correct information")
                
                return redirect('money_company_details', id=id)
            
            if 'phone_pe'in request.POST:
                amount = request.POST.get('phone_pe_amount')
                phonepe_number = request.POST.get('phonepe_number')
                date=request.POST.get('date')
                save_phonepe_company_amount(date, amount, e.shope_id, e.id,id, phonepe_number)
                return redirect('money_company_details', id=id)

            if 'bank'in request.POST:
                amount = request.POST.get('bank_amount')
                bank_number = request.POST.get('bank_number')
                date = request.POST.get('date')
                save_bank_company_amount(date, amount, e.shope_id, e.id,id, bank_number)
                return redirect('money_company_details', id=id)
            if 'edit_transition'in request.POST:
                t_id = request.POST.get('id')
                payment_type = request.POST.get('payment_type')
                bank_number = ''
                phonepe_number = ''
                if payment_type == 'Bank':
                    bank_number = request.POST.get('bank_number')
                elif payment_type == 'PhonePe':
                    phonepe_number = request.POST.get('phonepe_number')
                date = request.POST.get('date')
                amount = request.POST.get('amount')
                
                
                trans = company_recived_payment_transaction.objects.filter(id=t_id).first()
                o_m = trans.amount
                trans.payment_type = payment_type
                if payment_type == 'Bank':
                    trans.bank_number = bank_number
                    trans.phonepe_number = None
                elif payment_type == 'PhonePe':
                    trans.bank_number = None
                    trans.phonepe_number = phonepe_number
                else:
                    trans.bank_number = None
                    trans.phonepe_number = None
                trans.date = date
                trans.amount = amount
                trans.save()
                
                
                t = (int(o_m) - int(math.floor(float(amount))))
                bill = Company_bill.objects.filter(company_id=id, paid_status=1).order_by('-date')
                for b in bill:
                    if t > 0:
                        b.paid_status = 0
                        b.save()
                        t -= b.total_amount
                    else:
                        break
                return redirect('money_company_details', id=id)
                        
        context={ 
            'e':e,
            'company':Company.objects.filter(id=id).first(),
            'final_amount':final_amount,
            'recived_amount':recived_amount,
            'bill_amount':bill_amount,
            'transaction':company_recived_payment_transaction.objects.filter(company_id=id).order_by('payment_type','date'),
            'bill':Company_bill.objects.filter(company_id=id).order_by('-date'),
            'remening_amount':remening_amount,
            'today_date':datetime.date.today(),
            'opning_balance':Company_opning_balance.objects.filter(company_id=id).first()
        }
        return render(request, 'office/money_company_details.html', context)
    else:
        return redirect('login')
    
def change_company_bill_paid_status(company_id):
    b_opn = Company_opning_balance.objects.filter(company_id=company_id).first()
    print(b_opn)
    recived_payment = company_recived_payment_transaction.objects.filter(company_id=company_id).aggregate(Sum('amount'))['amount__sum']
    if b_opn:
        if b_opn.type == 0:
            recived_payment -= int(b_opn.balance)
        else:
            recived_payment += int(b_opn.balance)
   
    if recived_payment == None:
        recived_payment = 0
        
    paid_bill_amount = Company_bill.objects.filter(company_id=company_id, paid_status = 1).aggregate(Sum('total_amount'))['total_amount__sum']
    if paid_bill_amount == None:
        paid_bill_amount = 0
        
    remening_amount = (int(recived_payment) - int(paid_bill_amount))
    
    bill = Company_bill.objects.filter(company_id=company_id, paid_status=0).order_by('date')
    
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
    return {'bill_id':bill_id, 'remening_amount':remening_amount}
    
    
@csrf_exempt
def money_farmer_details(request,id):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile).first()
        
        if e:
            remening_amount = change_farmer_bill_paid_status(id)
            recived_amount = 0
            bill_amount = Farmer_bill.objects.filter(farmer_id=id).aggregate(Sum('total_amount'))['total_amount__sum']
            if bill_amount == None:
                bill_amount = 0
            
            recived_amount = Farmer_payment_transaction.objects.filter(shope_id=e.shope_id, farmer_id=id).aggregate(Sum('amount'))['amount__sum']
            if recived_amount == None:
                recived_amount = 0
                
            final_amount = int(bill_amount) - int(recived_amount)
            
            if 'cash'in request.POST:
                amount = request.POST.get('cash_amount')
                da = request.POST.get('date')
                if da and amount :
                    save_cash_farmer_amount(da, amount, e.shope_id, e.id,id)
                else:
                    messages.warning(request,"please insert correct information")
                
                return redirect('money_farmer_details', id=id)
            
            if 'phone_pe'in request.POST:
                amount = request.POST.get('phone_pe_amount')
                phonepe_number = request.POST.get('phonepe_number')
                date=request.POST.get('date')
                save_phonepe_farmer_amount(date, amount, e.shope_id, e.id,id, phonepe_number)
                return redirect('money_farmer_details', id=id)

            if 'bank'in request.POST:
                amount = request.POST.get('bank_amount')
                bank_number = request.POST.get('bank_number')
                date = request.POST.get('date')
                save_bank_farmer_amount(date, amount, e.shope_id, e.id,id, bank_number)
                return redirect('money_farmer_details', id=id)
        context={ 
            'e':e,
            'farmer':Farmer.objects.filter(id=id).first(),
            'final_amount':final_amount,
            'recived_amount':recived_amount,
            'bill_amount':bill_amount,
            'bill':Farmer_bill.objects.filter(farmer_id=id).order_by('-date'),
            'transaction':Farmer_payment_transaction.objects.filter(farmer_id=id).order_by('date'),
            'total_amount':Farmer_payment_transaction.objects.filter(farmer_id=id).aggregate(Sum('amount'))['amount__sum'],
            'remening_amount':remening_amount,
            'today_date':datetime.date.today()
        }
        return render(request, 'office/money_farmer_details.html', context)
    else:
        return redirect('login')

def change_farmer_bill_paid_status(farmer_id):
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
    return {'bill_id':bill_id, 'remening_amount':remening_amount}
    
def save_cash_farmer_amount(date, amount, shope_id, e_id,f_id):
    Farmer_payment_transaction(
        shope_id=shope_id,
        office_employee_id=e_id,
        farmer_id=f_id,
        amount=amount,
        payment_type='Cash',
        date=date
    ).save()
    
    
def save_phonepe_farmer_amount(date, amount, shope_id, e_id,f_id, phonepe_number):
    Farmer_payment_transaction(
        shope_id=shope_id,
        office_employee_id=e_id,
        farmer_id=f_id,
        amount=amount,
        phonepe_number=phonepe_number,
        payment_type='PhonePe',
        date=date
    ).save()


def save_bank_farmer_amount(date, amount, shope_id, e_id,f_id, bank_number):
    Farmer_payment_transaction(
        shope_id=shope_id,
        office_employee_id=e_id,
        farmer_id=f_id,
        amount=amount,
        bank_number=bank_number,
        payment_type='Bank',
        date=date
    ).save()
    
    
    
def save_bank_company_amount(date, amount, shope_id, e_id,c_id, bank_number):
        company_recived_payment_transaction(
            shope_id=shope_id,
            office_employee_id=e_id,
            company_id=c_id,
            amount=amount,
            bank_number=bank_number,
            payment_type='Bank',
            date=date
        ).save()
    
def save_phonepe_company_amount(date, amount, shope_id, e_id,c_id, phonepe_number):
    company_recived_payment_transaction(
        shope_id=shope_id,
        office_employee_id=e_id,
        company_id=c_id,
        amount=amount,
        phonepe_number=phonepe_number,
        payment_type='PhonePe',
        date=date
    ).save()
    
def save_cash_company_amount(date, amount, shope_id, e_id,c_id) :
    company_recived_payment_transaction(
        shope_id=shope_id,
        office_employee_id=e_id,
        company_id=c_id,
        amount=amount,
        payment_type='Cash',
        date=date
    ).save()
    
def report(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile).first()
        context={
            'e':e,
        }
        return render(request, 'office/report.html', context)
    else:
        return redirect('login')

@csrf_exempt
def edit_farmer_bill(request, id):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile).first()
        if e:
            edit_pin = '1'
            edit_status = 0
            bill = Farmer_bill.objects.filter(id=id).first()
            if request.session.has_key('edit_pin'):
                edit_pin = request.session['edit_pin']
                edit_status = 1
            if int(edit_pin) == int(e.shope.edit_pin):
                empty_box_weight = (bill.weight - bill.empty_box - bill.leaf_weight)
                if 'chang_farmer'in request.POST:
                    farmer_id = request.POST.get('farmer_id')
                    bill.farmer_id=farmer_id
                    bill.save()
                if 'edit_bill' in request.POST:
                    vehicale_number = request.POST.get('vehicale_number')
                    total_vehicale_weight = request.POST.get('total_vehicale_weight')
                    empty_vehicale_weight = request.POST.get('empty_vehicale_weight')
                    weight = request.POST.get('weight')
                    wasteage = request.POST.get('wasteage')
                    leaf_weight = request.POST.get('leaf_weight')
                    empty_box = request.POST.get('empty_box')
                    prise = request.POST.get('prise')
                    labor_amount = request.POST.get('labor')
                    total_amount = request.POST.get('total_amount')
                    bill.vehicale_number = vehicale_number
                    bill.total_vehicale_weight = total_vehicale_weight
                    bill.empty_vehicale_weight = empty_vehicale_weight
                    bill.weight = weight
                    bill.wasteage = wasteage
                    bill.leaf_weight = leaf_weight
                    bill.empty_box = empty_box
                    bill.prise = prise
                    bill.labor_amount = labor_amount
                    bill.total_amount = total_amount
                    bill.save()
                    
                    recived_payment = Farmer_payment_transaction.objects.filter(farmer_id=bill.farmer_id).aggregate(Sum('amount'))['amount__sum']
                    if recived_payment == None:
                        recived_payment = 0
                    paid_bill_amount = Farmer_bill.objects.filter(farmer_id=bill.farmer_id, paid_status = 1).aggregate(Sum('total_amount'))['total_amount__sum']
                    if paid_bill_amount == None:
                        paid_bill_amount = 0
                    remening_amount = (int(recived_payment) - int(paid_bill_amount))
                    bill = Farmer_bill.objects.filter(farmer_id=bill.farmer_id, paid_status=1).order_by('date')
                    
                    bill_id = 0
                    for b in bill:
                        if remening_amount <= b.total_amount:
                            b.paid_status = 0
                            b.save()
                            remening_amount -= b.total_amount
                    
                    del request.session['edit_pin']
                    return redirect(f'/office/view_farmer_bill/{id}')
            else:
                del request.session['office_mobile']
                return redirect('farmer_bill')
        else:
            return redirect('farmer_bill')
        context = {
            'e': e,
            'bill': Farmer_bill.objects.filter(id=id).first(),
            'empty_box_weight': empty_box_weight,
            'edit_status': edit_status,
            'farmer': Farmer.objects.filter(shope_id=e.shope.id)
        }
        return render(request, 'office/edit_farmer_bill.html', context)
    else:
        return redirect('login')
    
def company_bill_details(request, id):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile).first()
        company = Company.objects.filter(id=id).first()
        context={
            'e':e,
            'company':company,
            'bill':Company_bill.objects.filter(company_id=id).order_by('-id')
        }
        return render(request, 'office/company_details.html', context)
    else:
        return redirect('login')
    
def logo(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile).first()
        if 'logo'in request.POST:
            image = request.FILES.get('image')
            Logo(
                shope_id=e.shope.id,
                image=image
            ).save()
            return redirect('logo')
        if 'edit_logo'in request.POST:
            image = request.FILES.get('image')
            if image:
                Logo(
                    id=Logo.objects.filter(shope_id=e.shope.id).first().id,
                    shope_id=e.shope.id,
                    image=image
                ).save()
                return redirect('logo')
        context={
            'e':e,
            'l':Logo.objects.filter(shope_id=e.shope.id).first()
        }
        return render(request, 'office/logo.html', context)
    else:
        return redirect('login')
    
@csrf_exempt
def new_company_bill(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile).first()
        if 'complete_bill'in request.POST:
            
            company_id = request.POST.get('company_id')
            shope_id = e.shope.id
            vehicale_number = request.POST.get('vehicale_number')
            total_vehicale_weight = request.POST.get('total_vehicale_weight')
            empty_vehicale_weight = request.POST.get('empty_vehicale_weight')
            weight = request.POST.get('weight')
            empty_box = request.POST.get('empty_box')
            wasteage = request.POST.get('wasteage')
            prise = request.POST.get('prise')
            labor_amount = request.POST.get('labor')
            service_charge = request.POST.get('service_charge')
            eater = request.POST.get('eater')
            date = request.POST.get('date')
            leaf_weight = request.POST.get('leaf_weight') 
            total_amount = request.POST.get('total_amount')
            bill_number = Company_bill.objects.filter(shope_id=shope_id).count()
            bill_number += 1 
            # print('leaf_weight', int(math.floor(float(leaf_weight))))
            # print('total_vehicale_weight', total_vehicale_weight)
            # print('empty_vehicale_weight', empty_vehicale_weight)
            # print('company_id', company_id)
            # print('shope_id', shope_id)
            # print('e.id', e.id)
            # print('vehicale_number', vehicale_number)
            # print('weight', weight)
            # print('empty_box', empty_box)
            # print('wasteage', wasteage)
            # print('prise', prise)
            # print('total_amount', math.ceil(eval(total_amount)))
            # print('bill_number', bill_number)
            # print('labor_amount', labor_amount)
            # print('service_charge', service_charge)
            # print('eater', eater)
            # print('date', date)
            # print('------------------------------------------------')
            
            save_new_company_bill(
                int(math.floor(float(leaf_weight))),
                total_vehicale_weight,
                empty_vehicale_weight,
                company_id,
                shope_id,
                e.id,
                vehicale_number,
                weight,
                empty_box,
                wasteage,
                prise,
                math.ceil(eval(total_amount)),
                bill_number,
                labor_amount,
                service_charge,
                eater,
                date
            )
            f = Company_bill.objects.filter(shope_id=shope_id).last()
            return redirect(f'/office/view_company_bill/{f.id}')
            
        context={
            'e':e,
            'company':Company.objects.filter(shope_id=e.shope.id),
        }
        return render(request, 'office/new_company_bill.html', context)
    else:
        return redirect('login')
    
    
def save_new_company_bill(leaf_weight, total_vehicale_weight, empty_vehicale_weight, company_id, shope_id, employee_id, vehicale_number, weight, empty_box, wasteage, prise, total_amount, bill_number, labor_amount, service_charge, eater, date):
    # print('leaf_weight', leaf_weight)
    # print('total_vehicale_weight', total_vehicale_weight)
    # print('empty_vehicale_weight', empty_vehicale_weight)
    # print('company_id', company_id)
    # print('shope_id', shope_id)
    # print('employee_id', employee_id)
    # print('vehicale_number', vehicale_number)
    # print('weight', weight)
    # print('empty_box', empty_box)
    # print('wasteage', wasteage)
    # print('prise', prise)
    # print('total_amount', total_amount)
    # print('bill_number', bill_number)
    # print('labor_amount', labor_amount)
    # print('service_charge', service_charge)
    # print('eater', eater)
    # print('date', date)
    Company_bill(
        leaf_weight=leaf_weight,
        total_vehicale_weight=total_vehicale_weight,
        empty_vehicale_weight=empty_vehicale_weight,
        company_id=company_id,
        shope_id=shope_id,
        office_employee_id=employee_id,
        vehicale_number=vehicale_number,
        weight=weight,
        empty_box=empty_box,
        wasteage=wasteage,
        prise=prise,
        total_amount= total_amount,
        bill_number=bill_number,
        labor_amount=labor_amount,
        service_charge=service_charge,
        eater=eater,
        date=date
    ).save()
    
@csrf_exempt
def generate_company_bill_image(request, id):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        
        e = office_employee.objects.filter(mobile=mobile).first()
        bill = Company_bill.objects.filter(id=id).first()
        danda_weight_status = Company_services.objects.filter(shope_id=e.shope.id, name='Danda Weight').first()
        if danda_weight_status:
            danda_weight_status = danda_weight_status.status
        else:
            danda_weight_status = 0
        
        empty_box_weight = (bill.weight - bill.empty_box - bill.leaf_weight)
        wasteage_weight = (empty_box_weight + bill.wasteage)
        if (int(danda_weight_status) == 1):
            danda_weight = (wasteage_weight / 100) * 8
            total_weight = (wasteage_weight + danda_weight)
        else:
            danda_weight = 0
            total_weight = (wasteage_weight)
        amount = math.ceil(bill.prise * math.floor(total_weight))
        total_amount_words = num2words(bill.total_amount)
        signature = Signature.objects.filter(id=bill.office_employee.id).first()
        logo = Logo.objects.filter(shope_id=e.shope.id).first()
        
        recived_amount = company_recived_payment_transaction.objects.filter(shope_id=e.shope_id, company_id=bill.company.id).aggregate(Sum('amount'))['amount__sum']
        if recived_amount == None:
            recived_amount = 0
            
        bill_amount = Company_bill.objects.filter(company_id=bill.company.id).aggregate(Sum('total_amount'))['total_amount__sum']
        if bill_amount == None:
            bill_amount = 0
            
        final_amount = int(bill_amount) - int(recived_amount)
        context = {
            'e': e,
            'bill': bill,
            'empty_box_weight': empty_box_weight,
            'wasteage_weight': wasteage_weight,
            'danda_weight': danda_weight,
            'total_weight': total_weight,
            'amount': amount,
            'total_amount_words': total_amount_words,
            'signature': signature,
            'logo': logo,
            'final_amount':final_amount,
            'recived_amount':recived_amount,
            'bill_amount':bill_amount,
            'today_date':date.today(),
        }
        return render(request, 'office/generate_company_bill_image.html', context)
    else:
        return redirect('login')
    
@csrf_exempt
def generate_farmer_bill_image(request, id):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile).first()
        bill = Farmer_bill.objects.filter(id=id).first()
        empty_box_weight = (bill.weight - bill.empty_box - bill.leaf_weight)
        wasteage_weight = (empty_box_weight + bill.wasteage)
        danda_weight = (wasteage_weight / 100) * 8
        total_weight = (wasteage_weight + danda_weight)
        amount = math.ceil(bill.prise * math.floor(total_weight))
        total_amount_words = num2words(bill.total_amount)
        signature = Signature.objects.filter(id=bill.office_employee.id).first()
        logo = Logo.objects.filter(shope_id=e.shope.id).first()

        context = {
            'e': e,
            'bill': bill,
            'empty_box_weight': empty_box_weight,
            'wasteage_weight': wasteage_weight,
            'danda_weight': danda_weight,
            'total_weight': total_weight,
            'amount': amount,
            'total_amount_words': total_amount_words,
            'signature': signature,
            'logo': logo,
        }

        return render(request, 'office/generate_farmer_bill_image.html', context)
    else:
        return redirect('login')

@csrf_exempt
def view_company_bill(request, id):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile).first()
        
        
        danda_weight_status = Company_services.objects.filter(shope_id=e.shope.id, name='Danda Weight').first()
        if danda_weight_status:
            danda_weight_status = danda_weight_status.status
        else:
            danda_weight_status = 0
        
        total_pending_amount = 0
        
        bill = Company_bill.objects.filter(id=id).first()
        empty_box_weight = (bill.weight - bill.empty_box - bill.leaf_weight)
        wasteage_weight = (empty_box_weight + bill.wasteage)
        if (int(danda_weight_status) == 1):
            danda_weight = (wasteage_weight / 100) * 8
            total_weight = (wasteage_weight + danda_weight)
        else:
            danda_weight = 0
            total_weight = (wasteage_weight)
        amount = math.ceil(bill.prise * math.floor(total_weight))
        p = ''
        total_amount_words = num2words(bill.total_amount)
        signature = Signature.objects.filter(id=bill.office_employee.id).first()
        total_credit = 0
        total_pending_amount = bill.total_amount
    
        if bill.paid_status == 0:
            if total_pending_amount == 0:
                bill.paid_status = 1
                bill.save()
                return redirect(f'/office/view_company_bill/{bill.id}')
            
        recived_amount = company_recived_payment_transaction.objects.filter(shope_id=e.shope_id, company_id=bill.company.id).aggregate(Sum('amount'))['amount__sum']
        if recived_amount == None:
            recived_amount = 0
            
        bill_amount = Company_bill.objects.filter(company_id=bill.company.id).aggregate(Sum('total_amount'))['total_amount__sum']
        if bill_amount == None:
            bill_amount = 0
            
        final_amount = int(bill_amount) - int(recived_amount)

        context={
            'e':e,
            'bill':bill,
            'empty_box_weight':empty_box_weight,
            'wasteage_weight':wasteage_weight,
            'danda_weight':danda_weight,
            'total_weight':total_weight,
            'amount':amount,
            'final_amount':final_amount,
            'recived_amount':recived_amount,
            'bill_amount':bill_amount,
            'total_amount_words':total_amount_words,
            'signature':signature,
            'logo':Logo.objects.filter(shope_id=e.shope.id).first(),
            'total_pending_amount':total_pending_amount,
            'total_credit':total_credit,
            'danda_weight_status':danda_weight_status,
            'today_date':date.today(),
        }   
        return render(request, 'office/view_company_bill.html', context)

@csrf_exempt
def edit_company_bill(request, id):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile).first()
        if e:
            edit_pin = '1'
            edit_status = 0
            if request.session.has_key('edit_pin'):
                edit_pin = request.session['edit_pin']
                edit_status = 1
            if int(edit_pin) == int(e.shope.edit_pin):
                bill = Company_bill.objects.filter(id=id).first()
                empty_box_weight = (bill.weight - bill.empty_box - bill.leaf_weight)
                if 'chang_company'in request.POST:
                    company_id = request.POST.get('company_id')
                    bill.company_id=company_id
                    bill.save()
                if 'edit_bill'in request.POST:
                    vehicale_number = request.POST.get('vehicale_number')
                    total_vehicale_weight = request.POST.get('total_vehicale_weight')
                    empty_vehicale_weight = request.POST.get('empty_vehicale_weight')
                    weight = request.POST.get('weight')
                    empty_box = request.POST.get('empty_box')
                    wasteage = request.POST.get('wasteage')
                    prise = request.POST.get('prise')
                    labor_amount = request.POST.get('labor')
                    service_charge = request.POST.get('service_charge')
                    eater = request.POST.get('eater')
                    date = request.POST.get('date')
                    leaf_weight = request.POST.get('leaf_weight') 
                    total_amount = request.POST.get('total_amount')
                    
                    bill.leaf_weight=leaf_weight
                    bill.total_vehicale_weight=total_vehicale_weight
                    bill.empty_vehicale_weight=empty_vehicale_weight
                    bill.vehicale_number=vehicale_number
                    bill.weight=weight
                    bill.empty_box=empty_box
                    bill.wasteage=wasteage
                    bill.prise=prise
                    bill.total_amount= math.ceil(eval(total_amount))
                    bill.labor_amount=labor_amount
                    bill.service_charge=service_charge
                    bill.eater=eater
                    bill.date=date
                    bill.save()
                    
                    b_opn = Company_opning_balance.objects.filter(company_id=bill.company_id).first()
                    print(b_opn)
                    recived_payment = company_recived_payment_transaction.objects.filter(company_id=bill.company_id).aggregate(Sum('amount'))['amount__sum']
                    if b_opn:
                        if b_opn.type == 0:
                            recived_payment -= int(b_opn.balance)
                        else:
                            recived_payment += int(b_opn.balance)
                
                    if recived_payment == None:
                        recived_payment = 0
                        
                    paid_bill_amount = Company_bill.objects.filter(company_id=bill.company_id, paid_status = 1).aggregate(Sum('total_amount'))['total_amount__sum']
                    if paid_bill_amount == None:
                        paid_bill_amount = 0
                        
                    remening_amount = (int(recived_payment) - int(paid_bill_amount))
                    
                    bill = Company_bill.objects.filter(company_id=bill.company_id, paid_status=1).order_by('date')
                    
                    bill_id = 0
                    for b in bill:
                        if remening_amount <= b.total_amount:
                            b.paid_status = 0
                            b.save()
                            remening_amount -= b.total_amount
                        
                    del request.session['edit_pin']
                    
                    return redirect(f'/office/view_company_bill/{id}')
            else:
                del request.session['office_mobile']
                return redirect('company_bill')
        else:
            return redirect('company_bill')
        context={
            'e':e,
            'bill':Company_bill.objects.filter(id=id).first(),
            'empty_box_weight':empty_box_weight,
            'edit_status':edit_status,
            'company':Company.objects.filter(shope_id=e.shope_id, status=1),
            'danda_weight_status':Company_services.objects.filter(shope_id=e.shope.id, name='Danda Weight').first()
        }
        return render(request, 'office/edit_company_bill.html', context)
    else:
        return redirect('login')
    
def company_bill(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile).first()
        if 'check_pin'in request.POST: 
            id = request.POST.get('id')
            pin = request.POST.get('pin')
            if str(e.shope.edit_pin) == str(pin):
                request.session['edit_pin'] = request.POST["pin"]
                return redirect(f'/office/edit_company_bill/{id}')
            else:
                del request.session['office_mobile']
                messages.warning(request, "चुकीचा ' एडिट पीन  '")
                return redirect('company_bill')

        context={
            'e':e,
            'bill':Company_bill.objects.filter(shope_id=e.shope.id).order_by('-id'),
        }
        return render(request, 'office/company_bill.html', context)
    else:
        return redirect('login')
    
def company(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile).first()
        if 'Add_company'in request.POST:
            name = request.POST.get('name').upper()
            address = request.POST.get('address')
            if Company.objects.filter(shope_id=e.shope.id,name=name).exists():
                messages.warning(request, 'Company already exists')
            else:
                Company(
                    shope_id=e.shope.id,
                    name=name,
                    address=address,
                ).save()
            return redirect('/office/company/')
        if 'Edit_company'in request.POST:
            id = request.POST.get('id')
            name = request.POST.get('name').upper()
            address = request.POST.get('address')
            if Company.objects.filter(shope_id=e.shope.id,name=name).exclude(id=id).exists():
                messages.warning(request, "Company already exists")
            else:
                Company(
                    id=id,
                    shope_id=e.shope.id,
                    name=name,
                    address=address,
                ).save()
                return redirect('/office/company/')
        if 'active'in request.POST:
            id = request.POST.get('id')
            c = Company.objects.filter(id=id).first()
            c.status = 0
            c.save()
            return redirect('/office/company/')
        if 'deactive'in request.POST:
            id = request.POST.get('id')
            c = Company.objects.filter(id=id).first()
            c.status = 1
            c.save()
            return redirect('/office/company/')
        context={
            'e':e,
            'company':Company.objects.filter(shope_id=e.shope.id)           
        }
        return render(request, 'office/company.html', context)
    else:
        return redirect('login')
    
@csrf_exempt
def new_farmer_bill(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile).first()
        selected_farmer_status = 0
        farmer = ''
        if 'add_farmer'in request.POST:
            name = request.POST.get('name')
            address = request.POST.get('address')
            c_mobile = request.POST.get('mobile')
            if Farmer.objects.filter(shope_id=e.shope.id,mobile=c_mobile).exists():
                selected_farmer_status = 1
                farmer = Farmer.objects.filter(shope_id=e.shope.id,mobile=c_mobile).last()
            else:
                Farmer(
                    shope_id=e.shope.id,
                    name=name,
                    address=address,
                    mobile=c_mobile
                ).save()
                selected_farmer_status = 1
                farmer = Farmer.objects.filter(shope_id=e.shope.id,mobile=c_mobile).last()
        if 'select_farmer'in request.POST:
            fid = request.POST.get('farmer_id')
            selected_farmer_status = 1
            farmer = Farmer.objects.filter(id=fid).first()
        if 'complete_bill'in request.POST:
            farmer_id = request.POST.get('farmer_id')
            shope_id = e.shope.id
            date = request.POST.get('date')
            vehicale_number = request.POST.get('vehicale_number')
            total_vehicale_weight = request.POST.get('total_vehicale_weight')
            empty_vehicale_weight = request.POST.get('empty_vehicale_weight')
            weight = request.POST.get('weight')
            wasteage = request.POST.get('wasteage')
            leaf_weight = request.POST.get('leaf_weight')
            print('life_weight' , leaf_weight )
            empty_box = request.POST.get('empty_box')
            prise = request.POST.get('prise')
            labor_amount = request.POST.get('labor')
            total_amount = request.POST.get('total_amount')
            bill_number = Farmer_bill.objects.filter(shope_id=shope_id).count()
            bill_number += 1 
            Farmer_bill(
                total_vehicale_weight=total_vehicale_weight,
                empty_vehicale_weight=empty_vehicale_weight,
                farmer_id=farmer_id,
                shope_id=shope_id,
                office_employee_id=e.id,
                vehicale_number=vehicale_number,
                weight=weight,
                empty_box=empty_box,
                wasteage=wasteage,
                prise=prise,
                total_amount= math.ceil(eval(total_amount)),
                bill_number=bill_number,
                labor_amount=labor_amount,
                leaf_weight=int(math.floor(float(leaf_weight))),
                date=date
            ).save()
            f = Farmer_bill.objects.filter(shope_id=shope_id).last()
            return redirect(f'/office/view_farmer_bill/{f.id}')
        context={
            'e':e,
            'selected_farmer_status':selected_farmer_status,
            'farmer':farmer,
            'leaf_weight':Farmer_services.objects.filter(shope_id=e.shope.id,name='Leaf Weight').first(),
            'date_today':datetime.date.today(),
        }
        return render(request, 'office/new_farmer_bill.html', context)
    else:
        return redirect('login')
    
def farmer_bill(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile).first()
        if 'check_pin'in request.POST: 
            id = request.POST.get('id')
            pin = request.POST.get('pin')
            if str(e.shope.edit_pin) == str(pin):
                request.session['edit_pin'] = request.POST["pin"]
                return redirect(f'/office/edit_farmer_bill/{id}')
            else:
                del request.session['office_mobile']
                messages.warning(request, "चुकीचा ' एडिट पीन  '")
                return redirect('company_bill')
        context={
            'e':e,
            'bill':Farmer_bill.objects.filter(shope_id=e.shope.id).order_by('-id'),
            'all_users':office_employee.objects.filter(shope_id=e.shope.id)
        }
        return render(request, 'office/farmer_bill.html', context)
    else:
        return redirect('login')
    
@csrf_exempt
def view_farmer_bill(request, id):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile).first()

        bill = Farmer_bill.objects.filter(id=id).first()
        empty_box_weight = (bill.weight - bill.empty_box - bill.leaf_weight)
        wasteage_weight = (empty_box_weight + bill.wasteage)
        danda_weight = (wasteage_weight / 100) * 8
        total_weight = (wasteage_weight + danda_weight)
        amount = math.ceil(bill.prise * math.floor(total_weight))
        p = ''
        total_amount_words = num2words(bill.total_amount)
        
        signature = Signature.objects.filter(office_employee_id=bill.office_employee.id).first()

        total_credit = 0
        total_pending_amount = bill.total_amount
        context={
            'e':e,
            'bill':bill,
            'empty_box_weight':empty_box_weight,
            'wasteage_weight':wasteage_weight,
            'danda_weight':danda_weight,
            'total_weight':total_weight,
            'amount':amount,
            'total_amount_words':total_amount_words,
            'signature':signature,
            'total_credit':total_credit,
            'total_pending_amount':total_pending_amount,
            'logo':Logo.objects.filter(shope_id=e.shope.id).first(),
            'date_today':datetime.date.today(),
        }
        return render(request, 'office/view_farmer_bill.html', context)
    else:
        return redirect('login')
    
def add_employee(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile).first()
        if e:
            if 'Add_employee'in request.POST:
                name = request.POST.get('name')
                mobile = request.POST.get('mobile')
                pin = request.POST.get('pin')
                if office_employee.objects.filter(mobile=mobile).exists():
                    pass
                else:
                    office_employee(
                        shope_id=e.shope.id,
                        name=name,
                        mobile=mobile,
                        pin=pin,
                    ).save()    
                return redirect('/owner/add_employee/')
            if 'Edit_employee'in request.POST:
                id = request.POST.get('id')
                name = request.POST.get('name')
                mobile = request.POST.get('mobile')
                pin = request.POST.get('pin')
                office_employee(
                    id=id,
                    shope_id=e.shope.id,
                    name=name,
                    mobile=mobile,
                    pin=pin,
                ).save()
                return redirect('/office/add_employee/')
            if 'active'in request.POST:
                id = request.POST.get('id')
                c = office_employee.objects.filter(id=id).first()
                c.status = 0
                c.save()
                return redirect('/office/add_employee/')
            if 'deactive'in request.POST:
                id = request.POST.get('id')
                c = office_employee.objects.filter(id=id).first()
                c.status = 1
                c.save()
                return redirect('/office/add_employee/')
            
        else:
            del request.session['office_mobile']
            return redirect('login')
        context={
            'e':e,
            'office_employee':office_employee.objects.filter(shope_id=e.shope.id)
        }
        return render(request, 'office/add_employee.html', context)
    else:
        return redirect('login')
    
def profile(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile).first()
        if e:
            if 'edit_profile'in request.POST:
                shope_name = request.POST.get('shope_name')
                owner_name = request.POST.get('owner_name')
                address = request.POST.get('address')
                description = request.POST.get('description')
                contact_details = request.POST.get('contact_details')
                e.shope.shope_name = shope_name
                e.shope.owner_name = owner_name
                e.shope.address = address
                e.shope.description = description
                e.shope.contact_details = contact_details
                e.shope.save()

        else:
            del request.session['office_mobile']
            
        context={
            'e':e
        }
        return render(request, 'office/profile.html', context)
    else:
        return redirect('login')

def signature(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile).first()
        
        s = Signature.objects.filter(office_employee_id=e.id).first()
        if s == None:
            s = ''
        if 'add_signature'in request.POST:
            image = request.FILES.get("image")
            Signature(
                office_employee_id=e.id,
                image=image
            ).save()
            return redirect('signature')
        if 'edit_signature'in request.POST:
            image = request.FILES.get("image")
            if image:
                Signature(
                    id=s.id,
                    office_employee_id=e.id,
                    image=image
                ).save()
                return redirect('signature')
        context={
            'e':e,
            's':s
        }
        return render(request, 'office/signature.html', context)
    else:
        return redirect('login')

def farmer(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile).first()
        remaining_farmer = []
        compleated_farmer = []
        for f in Farmer.objects.filter(shope_id=e.shope.id).order_by('name'):
            order_by_status = 1
            completed_amount_total = Farmer_payment_transaction.objects.filter(farmer_id=f.id).aggregate(Sum('amount'))['amount__sum']
            if completed_amount_total == None:
                completed_amount_total = 0
            total = Farmer_bill.objects.filter(farmer_id=f.id).aggregate(Sum('total_amount'))['total_amount__sum']
            if total == None:
                total = 0
            t = (int(total) - int(completed_amount_total))
            
            if t < 1:
                order_by_status = 0
            
            if int(order_by_status) == 1:
                remaining_farmer.append({
                    'id':f.id,
                    'name':f.name,
                    'mobile':f.mobile,
                })
            else:
                compleated_farmer.append({
                    'id':f.id,
                    'name':f.name,
                    'mobile':f.mobile,
                })
        context={
            'e':e,
            'remaining_farmer':remaining_farmer,
            'compleated_farmer':compleated_farmer
        }
        return render(request, 'office/farmer.html', context)
    else:
        return redirect('login')