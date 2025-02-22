from django.db import models

# Create your models here.
class Shope(models.Model):
    shope_name = models.CharField(max_length=100)
    owner_name = models.CharField(max_length=100)
    mobile = models.IntegerField()
    address = models.CharField(max_length=500, null=True)
    description = models.CharField(max_length=500, null=True)
    contact_details = models.CharField(max_length=500, null=True)
    pin = models.IntegerField()
    edit_pin = models.IntegerField(default=1234)
    status = models.IntegerField(default=1)
    
class Shope_payment(models.Model):
    shope = models.ForeignKey(Shope, on_delete=models.CASCADE)
    amount = models.FloatField()
    from_date = models.DateField()
    to_date = models.DateField()
    payment_type = models.CharField(max_length=100)
    added_date = models.DateField(auto_now_add=True)