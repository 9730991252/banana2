from django.db import models
from sunil.models import *
from PIL import Image
# Create your models here.
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
    wasteage = models.IntegerField()
    prise = models.FloatField()
    total_amount = models.FloatField()
    paid_status = models.IntegerField(default=0)
    labor_amount = models.FloatField(null=True)
    date = models.DateField(auto_now_add=True)
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
        
class Farmer_cash_transition(models.Model):
    shope = models.ForeignKey(Shope,on_delete=models.PROTECT,null=True)
    office_employee = models.ForeignKey(office_employee,on_delete=models.PROTECT,null=True)
    farmer_bill = models.ForeignKey(Farmer_bill,on_delete=models.PROTECT,null=True)
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)
    added_date = models.DateTimeField(auto_now_add=True)

class Farmer_Phonepe_transition(models.Model):
    shope = models.ForeignKey(Shope,on_delete=models.PROTECT,null=True)
    office_employee = models.ForeignKey(office_employee,on_delete=models.PROTECT,null=True)
    farmer_bill = models.ForeignKey(Farmer_bill,on_delete=models.PROTECT,null=True)
    mobile = models.IntegerField(null=True)
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)
    added_date = models.DateTimeField(auto_now_add=True)

class Farmer_bank_transition(models.Model):
    shope = models.ForeignKey(Shope,on_delete=models.PROTECT,null=True)
    office_employee = models.ForeignKey(office_employee,on_delete=models.PROTECT,null=True)
    farmer_bill = models.ForeignKey(Farmer_bill,on_delete=models.PROTECT,null=True)
    bank_number = models.IntegerField(null=True)
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)
    added_date = models.DateTimeField(auto_now_add=True)
    
class Company(models.Model):
    shope = models.ForeignKey(Shope,on_delete=models.PROTECT,null=True)
    name = models.CharField(max_length=100)
    status = models.IntegerField(default=1)
    
class Company_bill(models.Model):
    shope = models.ForeignKey(Shope,on_delete=models.PROTECT,null=True)
    company = models.ForeignKey(Company,on_delete=models.PROTECT,null=True)
    farmer_bill = models.ForeignKey(Farmer_bill,on_delete=models.PROTECT,null=True)
    product_cost_rate = models.FloatField()
    product_cost_net_weight = models.FloatField()
    product_cost_box = models.FloatField()
    service_rate = models.FloatField()
    service_net_weight = models.FloatField()
    transport_rate = models.FloatField()
    transport_box = models.FloatField()
    stalk_rate = models.FloatField()
    stalk_net_weight = models.FloatField()
    wasteage_rate = models.FloatField()
    wastage_weight = models.FloatField()
    service_total_amount = models.FloatField()
    wasteage_total_amount = models.FloatField()
    product_cost_total_amount = models.FloatField()
    stalk_total_amount = models.FloatField()
    transport_total_amount = models.FloatField()
    total_amount = models.FloatField( null=True)
    company_bill_number = models.IntegerField(default=1)
    date=models.DateField(auto_now_add=True, null=True)
    added_date=models.DateTimeField(auto_now_add=True, null=True)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    