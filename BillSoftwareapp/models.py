from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    Company_code = models.CharField(max_length=100,null=True,blank=True)
    company_name = models.CharField(max_length=100,null=True,blank=True)
    address = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True)
    country = models.CharField(max_length=100,null=True,blank=True)
    contact = models.CharField(max_length=100,null=True,blank=True)
    pincode = models.IntegerField(null=True,blank=True)
    pan_number = models.CharField(max_length=255,null=True,blank=True)
    gst_type = models.CharField(max_length=255,null=True,blank=True)
    gst_no = models.CharField(max_length=255,null=True,blank=True)
    profile_pic = models.ImageField(null=True,blank = True,upload_to = 'image/patient')


class staff_details(models.Model):
    company = models.ForeignKey(company, on_delete=models.CASCADE,null=True,blank=True)
    first_name = models.CharField(max_length=100,null=True,blank=True)
    last_name = models.CharField(max_length=100,null=True,blank=True)
    email = models.CharField(max_length=100,null=True,blank=True)
    user_name = models.CharField(max_length=100,null=True,blank=True)
    password = models.CharField(max_length=100,null=True,blank=True)
    contact = models.CharField(max_length=255,null=True,blank=True)
    img = models.ImageField(null=True,blank = True,upload_to = 'image/staff')    
    position = models.CharField(max_length=255,null=True,blank=True,default='staff')


class ItemModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    company = models.ForeignKey(company,on_delete= models.CASCADE,null=True,blank=True)
    staff = models.ForeignKey(staff_details,on_delete= models.CASCADE,null=True,blank=True)
    item_name = models.CharField(max_length=255)
    item_hsn = models.PositiveIntegerField(null=True)
    item_unit = models.CharField(max_length=255)
    item_type = models.CharField(max_length=255)
    item_taxable = models.CharField(max_length=255)
    item_gst = models.CharField(max_length=255,null=True)
    item_igst = models.CharField(max_length=255,null=True)
    item_sale_price = models.PositiveIntegerField()
    item_current_stock = models.PositiveBigIntegerField(default=0)
    item_purchase_price = models.PositiveBigIntegerField()
    item_stock_in_hand = models.PositiveBigIntegerField(default=0)
    item_at_price = models.PositiveBigIntegerField(default=0)
    item_date = models.DateField()

class ItemUnitModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    company = models.ForeignKey(company,on_delete= models.CASCADE,null=True,blank=True)
    unit_name = models.CharField(max_length=255)

class ItemTransactionModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    company = models.ForeignKey(company,on_delete= models.CASCADE,null=True,blank=True)
    staff = models.ForeignKey(staff_details,on_delete= models.CASCADE,null=True,blank=True)
    item = models.ForeignKey(ItemModel,on_delete=models.CASCADE,null=True,blank=True)
    trans_type = models.CharField(max_length=255)
    trans_invoice = models.PositiveBigIntegerField(null=True,blank=True)
    trans_user_name = models.CharField(max_length=255)
    trans_date = models.DateTimeField()
    trans_qty = models.PositiveBigIntegerField(default=0)
    trans_current_qty = models.PositiveBigIntegerField(default=0)
    trans_adjusted_qty = models.PositiveBigIntegerField(default=0)
    trans_price = models.PositiveBigIntegerField(default=0)
    trans_status = models.CharField(max_length=255)
    trans_created_date = models.DateTimeField(auto_now_add=True,null=True)

class ItemTransactionHistory(models.Model):
    staff = models.ForeignKey(staff_details,on_delete=models.CASCADE,blank=True,null=True)
    company = models.ForeignKey(company,on_delete=models.CASCADE,blank=True,null=True)
    item = models.ForeignKey(ItemModel,on_delete=models.CASCADE,blank=True,null=True)
    date = models.DateField(auto_now_add=True,null=True)
    action = models.CharField(max_length=255)
    done_by_name = models.CharField(max_length=255)