from django.db import models

# Create your models here.
class Payment(models.Model):
    student = models.CharField(max_length=100,null=False,blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=False,blank=True, default=0)
    payment_method = models.CharField(max_length=100,null=False,blank=True)
    month = models.CharField(max_length=100,null=False,blank=True)
    academic_year = models.CharField(max_length=100,null=False,blank=True)
    status = models.CharField(max_length=30,null=False,default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
