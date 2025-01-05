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
            Company_bill(
                leaf_weight=leaf_weight,
                total_vehicale_weight=total_vehicale_weight,
                empty_vehicale_weight=empty_vehicale_weight,
                company_id=company_id,
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
                service_charge=service_charge,
                eater=eater,
                date=date
            ).save()
            f = Company_bill.objects.filter(shope_id=shope_id).last()
            return redirect(f'/office/view_company_bill/{f.id}')
            
        context={
            'e':e,
            'company':Company.objects.filter(shope_id=e.shope.id)
        }
        return render(request, 'office/new_company_bill.html', context)
    else:
        return redirect('login')
    
@csrf_exempt
def view_company_bill(request, id):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile).first()
        
        total_pending_amount = 0
        
        bill = Company_bill.objects.filter(id=id).first()
        empty_box_weight = (bill.weight - bill.empty_box - bill.leaf_weight)
        wasteage_weight = (empty_box_weight + bill.wasteage)
        danda_weight = (wasteage_weight / 100) * 8
        total_weight = (wasteage_weight + danda_weight)
        amount = math.ceil(bill.prise * math.floor(total_weight))
        p = ''
        total_amount_words = num2words(bill.total_amount)
        signature = Signature.objects.filter(id=bill.office_employee.id).first()
        total_credit = 0
        total_pending_amount = bill.total_amount
        
        cash = Company_cash_transition.objects.filter(company_bill_id=bill.id)
        cash_amount = 0
        for c in cash:
            total_credit += c.amount
            cash_amount += c.amount
            total_pending_amount -= c.amount
            
        p = Company_Phonepe_transition.objects.filter(company_bill_id=bill.id)
        phonepe_amount = 0
        for p in p:
            total_credit += p.amount
            phonepe_amount += p.amount
            total_pending_amount -= p.amount
            
        b = Company_bank_transition.objects.filter(company_bill_id=bill.id)
        bank_amount = 0
        for b in b:
            total_credit += b.amount
            bank_amount += b.amount
            total_pending_amount -= b.amount
        
        if 'save_cash_amount'in request.POST:
            amount = request.POST.get('cash_amount')
            Company_cash_transition(
                shope_id=e.shope.id,
                office_employee_id=e.id,
                company_bill_id=bill.id,
                amount=amount,
            ).save()
            return redirect(f'/office/view_company_bill/{bill.id}')
        
        if 'save_phonepe_amount'in request.POST:
            mobile = request.POST.get('mobile')
            amount = request.POST.get('amount')
            Company_Phonepe_transition(
                shope_id=e.shope.id,
                office_employee_id=e.id,
                company_bill_id=bill.id,
                mobile=mobile,
                amount=amount,
            ).save()
            return redirect(f'/office/view_company_bill/{bill.id}')        
        
        if 'save_bank_amount'in request.POST:
            bank_number = request.POST.get('bank_number')
            amount = request.POST.get('amount')
            Company_bank_transition(
                shope_id=e.shope.id,
                office_employee_id=e.id,
                company_bill_id=bill.id,
                bank_number=bank_number,
                amount=amount,
            ).save()
            return redirect(f'/office/view_company_bill/{bill.id}')
        if bill.paid_status == 0:
            if total_pending_amount == 0:
                bill.paid_status = 1
                bill.save()
                return redirect(f'/office/view_company_bill/{bill.id}')
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
            'logo':Logo.objects.filter(shope_id=e.shope.id).first(),
            'total_pending_amount':total_pending_amount,
            'cash':cash,
            'phonepe_transition':Company_Phonepe_transition.objects.filter(company_bill_id=bill.id),
            'bank_transition':Company_bank_transition.objects.filter(company_bill_id=bill.id),
            'cash_amount':cash_amount,
            'phonepe_amount':phonepe_amount,
            'bank_amount':bank_amount,
            'total_credit':total_credit

        }   
        return render(request, 'office/view_company_bill.html', context)

@csrf_exempt
def edit_company_bill(request, id):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile).first()
        if e:
            edit_pin = '1'
            if request.session.has_key('edit_pin'):
                edit_pin = request.session['edit_pin']
            if int(edit_pin) == int(e.shope.edit_pin):
                bill = Company_bill.objects.filter(id=id).first()
                empty_box_weight = (bill.weight - bill.empty_box - bill.leaf_weight)
                if 'edit_bill'in request.POST:
                    company_id = request.POST.get('company_id')
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
                    bill.company.id=company_id
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
                    return redirect(f'/office/view_company_bill/{id}')
                del request.session['edit_pin']
            else:
                del request.session['office_mobile']
                return redirect('company_bill')
        else:
            return redirect('company_bill')
        context={
            'e':e,
            'bill':Company_bill.objects.filter(id=id).first(),
            'empty_box_weight':empty_box_weight,

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
                leaf_weight=leaf_weight,
            ).save()
            f = Farmer_bill.objects.filter(shope_id=shope_id).last()
            return redirect(f'/office/view_farmer_bill/{f.id}')
        context={
            'e':e,
            'selected_farmer_status':selected_farmer_status,
            'farmer':farmer
        }
        return render(request, 'office/new_farmer_bill.html', context)
    else:
        return redirect('login')
    
def farmer_bill(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile).first()
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
        
        signature = Signature.objects.filter(id=bill.office_employee.id).first()
        total_credit = 0
        total_pending_amount = bill.total_amount
        
        cash = Farmer_cash_transition.objects.filter(farmer_bill_id=bill.id)
        for c in cash:
            total_credit += c.amount
            total_pending_amount -= c.amount
            
        p = Farmer_Phonepe_transition.objects.filter(farmer_bill_id=bill.id)
        for p in p:
            total_credit += p.amount
            total_pending_amount -= p.amount
            
        b = Farmer_bank_transition.objects.filter(farmer_bill_id=bill.id)
        for b in b:
            total_credit += b.amount
            total_pending_amount -= b.amount

        if bill.paid_status == 0:
            if total_pending_amount == 0:
                bill.paid_status = 1
                bill.save()
                return redirect(f'/office/view_farmer_bill/{bill.id}')
    
        if 'save_cash_amount'in request.POST:
            amount = request.POST.get('cash_amount')
            Farmer_cash_transition(
                shope_id=e.shope.id,
                office_employee_id=e.id,
                farmer_bill_id=bill.id,
                amount=amount,
            ).save()
            return redirect(f'/office/view_farmer_bill/{bill.id}')
        
        if 'save_phonepe_amount'in request.POST:
            mobile = request.POST.get('mobile')
            amount = request.POST.get('amount')
            Farmer_Phonepe_transition(
                shope_id=e.shope.id,
                office_employee_id=e.id,
                farmer_bill_id=bill.id,
                mobile=mobile,
                amount=amount,
            ).save()
            return redirect(f'/office/view_farmer_bill/{bill.id}')
        
        if 'save_bank_amount'in request.POST:
            bank_number = request.POST.get('bank_number')
            amount = request.POST.get('amount')
            Farmer_bank_transition(
                shope_id=e.shope.id,
                office_employee_id=e.id,
                farmer_bill_id=bill.id,
                bank_number=bank_number,
                amount=amount,
            ).save()
            return redirect(f'/office/view_farmer_bill/{bill.id}')
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
            'cash':cash,
            'phonepe_transition':Farmer_Phonepe_transition.objects.filter(farmer_bill_id=bill.id),
            'bank_transition':Farmer_bank_transition.objects.filter(farmer_bill_id=bill.id),
            'total_credit':total_credit,
            'total_pending_amount':total_pending_amount,
            'logo':Logo.objects.filter(shope_id=e.shope.id).first()
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
        context={
            'e':e,
            'farmer':Farmer.objects.filter(shope_id=e.shope.id).order_by('name'),
        }
        return render(request, 'office/farmer.html', context)
    else:
        return redirect('login')