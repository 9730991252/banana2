from django.db import models
from sunil.models import *
from PIL import Image
# Create your models here.
class Farmer_services(models.Model):
    shope = models.ForeignKey(Shope,on_delete=models.PROTECT,null=True)
    name = models.CharField(max_length=100)
    status = models.IntegerField(default=1)   
    
class Company_services(models.Model):
    shope = models.ForeignKey(Shope,on_delete=models.PROTECT,null=True)
    name = models.CharField(max_length=100)
    status = models.IntegerField(default=1) 
class office_employee(models.Model):
    shope = models.ForeignKey(Shope,on_delete=models.PROTECT,null=True)
    name = models.CharField(max_length=100)
    mobile = models.IntegerField()
    pin = models.IntegerField()
    status = models.IntegerField(default=1)
    
class Farmer(models.Model):
    shope = models.ForeignKey(Shope,on_delete=models.PROTECT,null=True)
    office_employee = models.ForeignKey(office_employee,on_delete=models.PROTECT,null=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200 , null=True)
    mobile = models.IntegerField()
    
class Farmer_bill(models.Model):
    farmer = models.ForeignKey(Farmer,on_delete=models.PROTECT,null=True)
    office_employee = models.ForeignKey(office_employee,on_delete=models.PROTECT,null=True)
    shope = models.ForeignKey(Shope,on_delete=models.PROTECT,null=True)
    vehicale_number = models.CharField(max_length=100)
    total_vehicale_weight = models.IntegerField(null=True)
    empty_vehicale_weight = models.IntegerField(null=True)
    weight = models.IntegerField()
    empty_box = models.IntegerField()
    leaf_weight = models.IntegerField(default=0)
    wasteage = models.IntegerField()
    prise = models.FloatField()
    total_amount = models.FloatField()
    paid_status = models.IntegerField(default=0)
    labor_amount = models.FloatField(null=True)
    date = models.DateField()
    bill_number = models.IntegerField(null=True)
    added_date = models.DateTimeField(auto_now_add=True)
    
class Signature(models.Model):
    office_employee = models.ForeignKey(office_employee,on_delete=models.PROTECT,null=True)
    image = models.ImageField(upload_to="images",default="",null=True, blank=True) 
    def save(self, *args,**kwargs):
        super().save(*args,**kwargs)
        image = Image.open(self.image.path)
        print('image...',image)
        output_size = (300,300)
        image.thumbnail(output_size)
        image.save(self.image.path)
        
class Logo(models.Model):
    shope = models.ForeignKey(Shope,on_delete=models.PROTECT,null=True)
    image = models.ImageField(upload_to="logo_images",default="",null=True, blank=True) 
    def save(self, *args,**kwargs):
        super().save(*args,**kwargs)
        image = Image.open(self.image.path)
        print('image...',image)
        output_size = (300,300)
        image.thumbnail(output_size)
        image.save(self.image.path)
    

class Company(models.Model):
    shope = models.ForeignKey(Shope,on_delete=models.PROTECT,null=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200 , null=True)
    status = models.IntegerField(default=1)
    
class Company_opning_balance(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, null=True)
    shope = models.ForeignKey(Shope,on_delete=models.PROTECT,null=True)
    balance = models.FloatField()
    type = models.IntegerField()
    added_date = models.DateTimeField(auto_now_add=True)
    
    
class Company_bill(models.Model):
    company = models.ForeignKey(Company,on_delete=models.PROTECT,null=True)
    office_employee = models.ForeignKey(office_employee,on_delete=models.PROTECT,null=True)
    shope = models.ForeignKey(Shope,on_delete=models.PROTECT,null=True)
    vehicale_number = models.CharField(max_length=100)
    total_vehicale_weight = models.IntegerField(null=True)
    empty_vehicale_weight = models.IntegerField(null=True)
    weight = models.IntegerField()
    empty_box = models.IntegerField()
    wasteage = models.IntegerField()
    prise = models.FloatField()
    total_amount = models.FloatField()
    paid_status = models.IntegerField(default=0)
    labor_amount = models.FloatField(null=True)
    service_charge = models.FloatField(null=True)
    eater = models.FloatField(null=True)
    date = models.DateField(null=True)
    bill_number = models.IntegerField(null=True)
    added_date = models.DateTimeField(auto_now_add=True)
    leaf_weight=models.IntegerField(default=0)
    
    
    
class company_recived_payment_transaction(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, null=True)
    shope = models.ForeignKey(Shope,on_delete=models.PROTECT,null=True)
    office_employee = models.ForeignKey(office_employee,on_delete=models.PROTECT,null=True)
    amount = models.FloatField()
    bank_number = models.IntegerField(null=True)
    phonepe_number = models.IntegerField(null=True)
    payment_type = models.CharField(max_length=100)
    date = models.DateField()
    added_date = models.DateTimeField(auto_now_add=True)
    

class Farmer_payment_transaction(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.PROTECT, null=True)
    shope = models.ForeignKey(Shope,on_delete=models.PROTECT,null=True)
    office_employee = models.ForeignKey(office_employee,on_delete=models.PROTECT,null=True)
    amount = models.FloatField()
    bank_number = models.IntegerField(null=True)
    phonepe_number = models.IntegerField(null=True)
    payment_type = models.CharField(max_length=100)
    date = models.DateField()
    added_date = models.DateTimeField(auto_now_add=True)