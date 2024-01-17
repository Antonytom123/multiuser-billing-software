from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from . models import *
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required
from django.utils.text import capfirst
from datetime import date
from django.template.response import TemplateResponse
from django.http.response import JsonResponse



# Create your views here.

def home(request):
  return render(request, 'home.html')


def about(request):
  return render(request, 'about.html')

def contact(request):
  return render(request, 'contact.html')


def service(request):
  return render(request, 'service.html')


def homepage(request):
  sid = request.session.get('staff_id')
  staff =  staff_details.objects.get(id=sid)
  cmp = company.objects.get(id=staff.company.id)
  context={
   'staff':staff,
    'cmp':cmp,
  }
  return render(request, 'companyhome.html',context)


def staffhome(request):
  sid = request.session.get('staff_id')
  staff =  staff_details.objects.get(id=sid)
  cmp = company.objects.get(id=staff.company.id)
  context={
   'staff':staff,
    'cmp':cmp,
  }
  return render(request, 'staffhome.html',context)

def register(request):
  return render(request, 'register.html')

def registercompany(request):
  return render(request, 'registercompany.html')

def registerstaff(request):
  return render(request, 'registerstaff.html')

def login(request):
  return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')



def registeruser(request):
    if request.method == 'POST':
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        user_name = request.POST['username']
        email_id = request.POST['email']
        mobile = request.POST['phoneno']
        passw = request.POST['pass']
        c_passw = request.POST['re_pass']
        profile_pic = request.FILES.get('image')

        # Additional validation checks
        if passw != c_passw:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        if User.objects.filter(username=user_name).exists():
            messages.error(request, 'Sorry, Username already exists')
            return redirect('register')

        if User.objects.filter(email=email_id).exists():
            messages.error(request, 'Sorry, Email already exists')
            return redirect('register')

        # if not email_id.endswith('@gmail.com'):
        #     messages.error(request, 'Invalid email address')
        #     return redirect('register')

        user_data = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=user_name,
            email=email_id,
            password=passw
        )
        user_data.save()

        data = User.objects.get(id=user_data.id)
        cust_data = company(contact=mobile, profile_pic=profile_pic, user=data)
        cust_data.save()

        demo_staff = staff_details(
            company=cust_data,
            email=email_id,
            position='company',
            user_name=user_name,
            password=passw,
            contact=mobile
        )
        demo_staff.save()

        # messages.success(request, 'Registration successful')
        return redirect('registercompany')

    return render(request, 'register.html')


def add_company(request):
    if request.method == 'POST':
        email = request.POST['email']
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Error: User with the specified email does not exist.')
            return render(request, 'registercompany.html')

        c = company.objects.get(user=user)
        c.company_name = request.POST['companyname']
        if company.objects.filter(company_name=c.company_name).exists():
            messages.error(request, 'Error: Company with the specified name already exists.')
            return render(request, 'registercompany.html')
        c.address = request.POST['address']
        c.city = request.POST['city']
        c.state = request.POST['state']
        c.country = request.POST['country']
        c.pincode = request.POST['pincode']
        c.pan_number = request.POST['pannumber']
        c.gst_type = request.POST['gsttype']
        c.gst_no = request.POST['gstno']

        code = get_random_string(length=6)
        if company.objects.filter(Company_code=code).exists():
            code2 = get_random_string(length=6)
            c.Company_code = code2
        else:
            c.Company_code = code
        
        c.save()

        staff = staff_details.objects.get(email=email, position='company', company=c)
        staff.first_name = request.POST['companyname']
        staff.last_name = ''
        staff.save()

        return redirect('login')  

    return render(request, 'registercompany.html')


def staff_registraction(request):
  if request.method == 'POST':
    fn=request.POST['fname']
    ln=request.POST['lname']
    email=request.POST['email']
    un=request.POST['username']
    ph=request.POST['phoneno']
    pas=request.POST['pass']
    code=request.POST['companycode']

    if company.objects.filter(Company_code=code).exists():
      com=company.objects.get(Company_code=code)
    else:
        messages.info(request, 'Sorry, Company code is Invalid')
        return redirect('registerstaff')
    img=request.FILES.get('image')

    if staff_details.objects.filter(user_name=un,company=com).exists():
      messages.info(request, 'Sorry, Username already exists')
      return redirect('registerstaff')
    elif staff_details.objects.filter(email=email,company=com).exists():
      messages.info(request, 'Sorry, Email already exists')
      return redirect('registerstaff')
    elif staff_details.objects.filter(contact=ph,company=com).exists():
      messages.info(request, 'Sorry, Phone Number already exists')
      return redirect('registerstaff')
    elif staff_details.objects.filter(password=pas).exists():
      messages.info(request, 'Sorry, Password already exists,please use another password')
      return redirect('registerstaff')
    else:
      
      staff=staff_details(first_name=fn,last_name=ln,email=email,user_name=un,contact=ph,password=pas,img=img,company=com)
      staff.save()
      return redirect('login')

  else:
    print(" error")
    return redirect('registerstaff')
  

  
def loginurl(request):
  if request.method == 'POST':
    user_name = request.POST['username']
    passw = request.POST['pass']
    
    
    log_user = auth.authenticate(username = user_name,
                                  password = passw)
    
    if log_user is not None:
      auth.login(request, log_user)
        
    if staff_details.objects.filter(user_name=user_name,password=passw,position='company').exists():
      data = staff_details.objects.get(user_name=user_name,password=passw,position='company') 

      request.session["staff_id"]=data.id
      if 'staff_id' in request.session:
        if request.session.has_key('staff_id'):
          staff_id = request.session['staff_id']
          print(staff_id)
 
        return redirect('homepage')  

    if staff_details.objects.filter(user_name=user_name,password=passw,position='staff').exists():
      data = staff_details.objects.get(user_name=user_name,password=passw,position='staff')   

      request.session["staff_id"]=data.id
      if 'staff_id' in request.session:
        if request.session.has_key('staff_id'):
          staff_id = request.session['staff_id']
          print(staff_id)
 
          return redirect('staffhome')  
    else:
      messages.info(request, 'Invalid Username or Password. Try Again.')
      return redirect('login')  
  else:  
   return redirect('login')   
  
  

@login_required(login_url='login')  
def profile(request):
    if request.user.is_authenticated:
        try:
            com = company.objects.get(user=request.user)
            staff_id = request.session['staff_id']
            staff =  staff_details.objects.get(id=staff_id)
            context = {
               'company': com,
               'staff':staff
               }
            return render(request, 'profile.html', context)
        except company.DoesNotExist:
            messages.error(request, 'Company not found for the authenticated user.')
            return redirect('login')
    else:
        messages.info(request, 'Please log in to view your profile.')
        return redirect('login')

    

def editprofile(request,pk):
  com= company.objects.get(id = pk)
  context={
     'company':com
  }
  return render(request, 'editprofile.html',context)

def edit_profilesave(request,pk):
  com= company.objects.get(id = pk)
  user1 = User.objects.get(id = com.user_id)

  if request.method == "POST":

      user1.first_name = capfirst(request.POST.get('f_name'))
      user1.last_name  = capfirst(request.POST.get('l_name'))
      user1.email = request.POST.get('email')
      com.contact = request.POST.get('cnum')
      com.address = capfirst(request.POST.get('ards'))
      com.company_name = request.POST.get('comp_name')
      # user1.email = request.POST.get('comp_email')
      com.city = request.POST.get('city')
      com.state = request.POST.get('state')
      com.country = request.POST.get('country')
      com.pincode = request.POST.get('pinc')
      com.gst_type = request.POST.get('gsttype')
      com.gst_no = request.POST.get('gstno')
      com.pan_number = request.POST.get('pan')
      if len(request.FILES)!=0 :
          com.profile_pic = request.FILES.get('file')
          

      com.save()
      user1.save()
      return redirect('profile')

  context = {
      'company' : com,
      'user1' : user1,
  } 

  return render(request,'editprofile.html',context)

def base(request):
  staff_id = request.session['staff_id']
  staff =  staff_details.objects.get(id=staff_id)
  context = {
              'staff' : staff

          }
  return render(request, 'base.html',context)

def staffprofile(request):
  staff_id = request.session['staff_id']
  staff =  staff_details.objects.get(id=staff_id)
  context = {
              'staff' : staff

          }
  return render(request,'profilestaff.html',context)

def editstaffprofile(request):
  staff_id = request.session['staff_id']
  staff =  staff_details.objects.get(id=staff_id)
  context={
     'staff':staff
  }
  return render(request, 'editstaff.html',context)

def edit_staffprofilesave(request):
  staff_id = request.session['staff_id']
  staff =  staff_details.objects.get(id=staff_id)

  if request.method == "POST":

      staff.first_name = capfirst(request.POST.get('f_name'))
      staff.last_name  = capfirst(request.POST.get('l_name'))
      staff.email = request.POST.get('email')
      staff.contact = request.POST.get('cnum')
      if len(request.FILES)!=0 :
          staff.img = request.FILES.get('file')

      staff.save()
      return redirect('staffprofile')

  context = {
      'staff' : staff
  } 

  return render(request,'editstaff.html',context)

def add_item(request):
  sid = request.session.get('staff_id')
  staff =  staff_details.objects.get(id=sid)
  cmp = company.objects.get(id=staff.company.id)
  todate = date.today()
  tdate = todate.strftime("%Y-%m-%d")
  item_units = ItemUnitModel.objects.filter(company = cmp)
  context={
    'staff':staff,
    'cmp':cmp,
    'date':tdate,
    'item_units':item_units
  }
  return render(request, 'add_item.html',context)


def item_create_new(request):
    if request.method == 'POST':
        sid = request.session.get('staff_id')
        staff = staff_details.objects.get(id=sid)
        cmp = company.objects.get(id=staff.company.id)

        item_name = request.POST.get('item_name')
        item_hsn = request.POST.get('item_hsn')

        if ItemModel.objects.filter(item_name=item_name, company=cmp).exists() or \
                ItemModel.objects.filter(item_hsn=item_hsn, company=cmp).exists():
            messages.error(request, 'Item Name or HSN already exists. Please choose a different Name or HSN.')
            return render(request, 'add_item.html')
        if len(item_hsn) < 6:
            messages.error(request, 'Item HSN must be 6 digits or more.')
            return render(request, 'add_item.html')

        item_unit = request.POST.get('item_unit')
        item_type = request.POST.get('type')
        item_taxable = request.POST.get('item_taxable')
        item_gst = request.POST.get('item_gst')
        item_igst = request.POST.get('item_igst')
        item_sale_price = request.POST.get('saleprice')
        item_purchase_price = request.POST.get('purprice')
        item_opening_stock = request.POST.get('item_opening_stock')
        item_current_stock = item_opening_stock
        if item_opening_stock == '' or None:
            item_opening_stock = 0
            item_current_stock = 0
        item_at_price = request.POST.get('item_at_price')
        if item_at_price == '' or None:
            item_at_price = 0
        item_date = request.POST.get('itmdate')

        item_data = ItemModel(user=staff.company.user,
                              company=cmp,
                              staff=staff,
                              item_name=item_name,
                              item_hsn=item_hsn,
                              item_unit=item_unit,
                              item_type=item_type,
                              item_taxable=item_taxable,
                              item_gst=item_gst,
                              item_igst=item_igst,
                              item_sale_price=item_sale_price,
                              item_purchase_price=item_purchase_price,
                              item_stock_in_hand=item_opening_stock,
                              item_current_stock=item_current_stock,
                              item_at_price=item_at_price,
                              item_date=item_date)
        item_data.save()

        tr_history = ItemTransactionHistory(company=cmp,
                                            staff=staff,
                                            item=item_data,
                                            action="CREATED",
                                            done_by_name=staff.first_name,)
        tr_history.save()

        if request.POST.get('save_and_next'):
            return redirect('add_item')
        elif request.POST.get('itemsave'):
            return redirect('view_item')

    return render(request, 'add_item.html')



def view_item(request):
  sid = request.session.get('staff_id')
  staff =  staff_details.objects.get(id=sid)
  cmp = company.objects.get(id=staff.company.id)
  allitem = ItemModel.objects.filter(company=cmp)
  # for i in allitem:
  #     last_transaction = ItemTransactionHistory.objects.filter(item=i).last()
  #     if last_transaction:
  #         i.action = last_transaction.action
  #         i.done_by_name = last_transaction.done_by_name
  #     else:
  #         i.action = None
  #         i.done_by_name = None

  context={
    'staff':staff,
    'cmp':cmp,
    'allitem':allitem,
  }
  return render(request, 'view_item.html',context)

def view_items(request, pk):
    sid = request.session.get('staff_id')
    staff = staff_details.objects.get(id=sid)
    cmp = company.objects.get(id=staff.company.id)
    allitem = ItemModel.objects.filter(company=cmp)
    items = ItemModel.objects.get(id=pk)
    if pk == 0:
      first_item = allitem.filter().first()
    else:
      first_item = allitem.get(id=pk)
      transactions = ItemTransactionModel.objects.filter(company = cmp,item=first_item.id).order_by('-trans_created_date')
      

    # last_transaction = ItemTransactionHistory.objects.filter(item=items).last()
    # if last_transaction:
    #     items.action = last_transaction.action
    #     items.done_by_name = last_transaction.done_by_name
    # else:
    #     items.action = None
    #     items.done_by_name = None

    context = {
        'staff': staff,
        'cmp': cmp,
        'item': items,
        'first_item':first_item,
        'allitem':allitem,
        'transactions':transactions,
        'item_name': items.item_name,
    }

    return render(request, 'view_items.html', context)


def edit_item(request,pk):
  sid = request.session.get('staff_id')
  staff = staff_details.objects.get(id=sid)
  cmp = company.objects.get(id=staff.company.id)
  allitem = ItemModel.objects.filter(company=cmp)
  items = ItemModel.objects.get(id=pk)

  context = {
        'staff': staff,
        'cmp': cmp,
        'item': items,
        'allitem':allitem
    }

  return render(request, 'edit_item.html',context)


# def update_item(request,pk):
#   if request.method=='POST':
#     sid = request.session.get('staff_id')
#     staff =  staff_details.objects.get(id=sid)
#     cmp = company.objects.get(id=staff.company.id)
#     item = ItemModel.objects.get(id=pk)

#     item.item_name = request.POST.get('item_name')
#     item.item_hsn = request.POST.get('item_hsn')
#     item.item_unit = request.POST.get('item_unit')
#     item.item_type = request.POST.get('type')
#     item.item_taxable = request.POST.get('item_taxable')
#     item.item_gst = request.POST.get('item_gst')
#     item.item_igst = request.POST.get('item_igst')
#     item.item_sale_price = request.POST.get('saleprice')
#     item.item_purchase_price = request.POST.get('purprice')
#     item.item_stock_in_hand = request.POST.get('item_opening_stock')
#     item.item_current_stock =item.item_stock_in_hand
#     item.item_at_price = request.POST.get('item_at_price')
#     item.item_date = request.POST.get('itmdate')
    
#     item.save()

#     tr_history = ItemTransactionHistory(company=cmp,
#                                             staff=staff,      
#                                             item=item,
#                                             action="UPDATED",
#                                             done_by_name=staff.first_name,
#                                             )
#     tr_history.save()
  

#     return redirect('view_item')
#   return redirect('edit_item')

def update_item(request, pk):
    if request.method == 'POST':
        sid = request.session.get('staff_id')
        staff = staff_details.objects.get(id=sid)
        cmp = company.objects.get(id=staff.company.id)

        item_data = ItemModel.objects.get(id=pk)
        user = cmp.user
        company_user_data = cmp

        item_name = request.POST.get('item_name')
        item_hsn = request.POST.get('item_hsn')
        item_unit = request.POST.get('item_unit')
        item_type = request.POST.get('type')
        item_taxable = request.POST.get('item_taxable')
        item_gst = request.POST.get('item_gst')
        item_igst = request.POST.get('item_igst')
        
        if item_taxable == 'Non Taxable':
            item_gst = 'GST0[0%]'
            item_igst = 'IGST0[0%]'

        item_sale_price = request.POST.get('saleprice')
        item_purchase_price = request.POST.get('purprice')
        item_stock_in_hand = request.POST.get('item_opening_stock')

        if item_stock_in_hand == '':
            item_stock_in_hand = 0

        item_current_stock = item_data.item_current_stock

        if int(item_stock_in_hand) > item_data.item_stock_in_hand:
            item_stock = item_data.item_current_stock + (int(item_stock_in_hand) - item_data.item_stock_in_hand)
        elif int(item_stock_in_hand) < item_data.item_stock_in_hand:
            item_stock = item_data.item_current_stock - (item_data.item_stock_in_hand - int(item_stock_in_hand))
        else:
            item_stock = item_current_stock

        item_at_price = request.POST.get('item_at_price')

        if item_at_price == '':
            item_at_price = 0

        item_date = request.POST.get('itmdate')

        item_data.user = user
        item_data.company = company_user_data
        item_data.item_name = item_name
        item_data.item_hsn = item_hsn
        item_data.item_unit = item_unit
        item_data.item_type = item_type
        item_data.item_taxable = item_taxable
        item_data.item_gst = item_gst
        item_data.item_igst = item_igst
        item_data.item_sale_price = item_sale_price
        item_data.item_purchase_price = item_purchase_price
        item_data.item_stock_in_hand = item_stock_in_hand
        item_data.item_current_stock = int(item_stock)
        item_data.item_at_price = item_at_price
        item_data.item_date = item_date

        item_data.save()
        print('\nupdated')

        tr_history = ItemTransactionHistory(company=cmp,
                                        staff=staff,      
                                        item=item_data,
                                        action="UPDATED",
                                        done_by_name=staff.first_name,
                                        )
        tr_history.save()

    return redirect('view_item')



def item_delete(request,pk):
  item_to_delete = ItemModel.objects.get(id=pk)
  item_to_delete.delete()
  return redirect('view_item')

def itemhistory(request,pk):
  staff_id = request.session['staff_id']
  staff =  staff_details.objects.get(id=staff_id)
  cmp = company.objects.get(id=staff.company.id)
  history = ItemTransactionHistory.objects.filter(item=pk)

  context = {
              'staff' : staff,
              'history':history,

          }
  return render(request,'itemtranstationhistory.html',context)

def itemmodaladjust(request,pk):
  item = ItemModel.objects.get(id=pk)
  return TemplateResponse(request,'itemmodaladjust.html',{"item":item,})


def ajust_quantity(request,pk):
  sid = request.session.get('staff_id')
  staff =  staff_details.objects.get(id=sid)
  cmp = company.objects.get(id=staff.company.id)

  if request.method=='POST':
    item = ItemModel.objects.get(id=pk)

    # user = User.objects.get(id=request.user.id)
    user = cmp.user
    # company_user_data = company.objects.get(user=request.user.id)
    company_user_data = cmp

    trans_type_check_checked = request.POST.get('trans_type')
    if trans_type_check_checked == 'on':
      trans_type = 'reduce stock'
      trans_qty = request.POST.get('reduced_qty')
    else:
      trans_type = 'add stock'
      trans_qty = request.POST.get('added_qty')
    trans_user_name = user.first_name
    trans_date = request.POST.get('trans_date')

    trans_adjusted_qty= request.POST.get('adjusted_qty')
    trans_current_qty = request.POST.get('item_qty')
    print(f'the quantity : {trans_current_qty}')
    item.item_current_stock = trans_adjusted_qty
    item.save()
    transaction_data = ItemTransactionModel(user=user,
                                        company=company_user_data,
                                        staff=staff,
                                        item=item,
                                        trans_type=trans_type,
                                        trans_user_name=trans_user_name,
                                        trans_date=trans_date,
                                        trans_qty=trans_qty,
                                        trans_current_qty=trans_current_qty,
                                        trans_adjusted_qty=trans_adjusted_qty,)
    transaction_data.save()
  return redirect('view_items',pk=item.id)

def item_unit_create(request):
  if request.method=='POST':
    #updated-shemeem
    sid = request.session.get('staff_id')
    staff =  staff_details.objects.get(id=sid)
    cmp = company.objects.get(id=staff.company.id)

    # user = User.objects.get(id=request.user.id)
    # company_user_data = company.objects.get(user=request.user.id)

    item_unit_name = request.POST.get('item_unit_name')
    unit_data = ItemUnitModel(user=cmp.user,company=cmp,unit_name=item_unit_name)
    unit_data.save()
  return redirect('add_item')


def edititemmodaladjust(request,pk,trans):
  item = ItemModel.objects.get(id=pk)
  transaction = ItemTransactionModel.objects.get(id=trans)
  print('enterd')
  return render(request,'edititemmodaladjust.html',{"item":item,"transaction":transaction,})

def update_adjusted_transaction(request,pk,trans):
  item = ItemModel.objects.get(id=pk)
  transaction = ItemTransactionModel.objects.get(id=trans)
  sid = request.session.get('staff_id')
  staff =  staff_details.objects.get(id=sid)
  cmp = company.objects.get(id=staff.company.id)

  if request.method=='POST':
    item = ItemModel.objects.get(id=pk)

    user = cmp.user
    company_user_data = cmp

    trans_type_check_checked = request.POST.get('trans_type')
    if trans_type_check_checked == 'on':
      trans_type = 'reduce stock'
      trans_qty = request.POST.get('reduced_qty')
    else:
      trans_type = 'add stock'
      trans_qty = request.POST.get('added_qty')
    trans_user_name = user.first_name
    trans_date = request.POST.get('trans_date')

    adjusted_qty= request.POST.get('adjusted_qty')
    trans_current_qty = request.POST.get('item_qty')
    if transaction.trans_type == 'reduce stock':
      if trans_type == 'reduce stock':
        print('reduce to reduce')
        item.item_current_stock = item.item_current_stock - (int(trans_qty)  - transaction.trans_qty)
      else:
        print('reduce to add')
        print(f'{trans_qty}-{transaction.trans_qty}={((int(trans_qty)  - transaction.trans_qty))}')
        item.item_current_stock = item.item_current_stock + transaction.trans_qty + int(trans_qty)
    else:
      if trans_type == 'reduce stock':
        print('add to red')
        item.item_current_stock = item.item_current_stock - (int(trans_qty)  + transaction.trans_qty)
      else:
        print('add to add')
        print(f'{trans_qty}-{transaction.trans_qty}={((int(trans_qty)  - transaction.trans_qty))}')
        item.item_current_stock = item.item_current_stock - transaction.trans_qty + int(trans_qty)
    # item.item_opening_stock = adjusted_qty
    item.save()
    transaction.trans_type =trans_type
    transaction.trans_date=trans_date
    transaction.trans_qty =trans_qty
    transaction.trans_current_qty=trans_current_qty
    transaction.save()
  return redirect('view_items',pk=item.id)

def transaction_delete(request,pk):
  transaction = ItemTransactionModel.objects.get(id=pk)
  item = ItemModel.objects.get(id=transaction.item_id)
  print(transaction.trans_type)
  if transaction.trans_type=='add stock':
    print('add')
    item.item_current_stock = item.item_current_stock - transaction.trans_qty
    print(item.item_name)
    print(item.item_current_stock)
    print(item.item_current_stock)
    print(transaction.trans_qty)
    print(item.item_current_stock - transaction.trans_qty)
  else:
    print('reduce')
    item.item_current_stock = item.item_current_stock + transaction.trans_qty
  item.save()
  transaction.delete()
  return redirect('view_items',pk=item.id)

def item_delete_openstock(request,pk):
  item = ItemModel.objects.get(id=pk)
  if item.item_stock_in_hand > item.item_current_stock:
    item.item_current_stock =item.item_stock_in_hand - item.item_current_stock
  else:
    item.item_current_stock =item.item_current_stock - item.item_stock_in_hand
  # item.item_current_stock =  item.item_opening_stock - item.item_current_stock
  item.item_stock_in_hand = 0
  # print(f'{item.item_current_stock }={item.item_opening_stock}-{item.item_current_stock}')
  item.save()
  return redirect('view_items',pk=item.id)