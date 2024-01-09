from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, cart, OrderPlaced
from .forms import CustomerRegistrationForm , CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required   #for function base-view
from django.utils.decorators import method_decorator   #for class base-view

class ProductView(View):
 def get(self, request):
  topwears = Product.objects.filter(category='TW')
  bottomwears = Product.objects.filter(category='BW')
  mobiles = Product.objects.filter(category = 'M')
  return render(request,'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles})
 

class ProductDetailView(View):
 def get(self, request, pk):
  product = Product.objects.get(pk=pk)
  item_already_in_cart=False
  if request.user.is_authenticated:
    item_already_in_cart= cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
  return render(request, 'app/productdetail.html',{'product':product, 'item_already_in_cart':item_already_in_cart})

@login_required
def add_to_cart(request):
 user = request.user
 product_id = request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 cart(user=user,product=product).save()
 return redirect('/cart')

@login_required
def show_cart(request):
  if request.user.is_authenticated:
    user = request.user
    cartt = cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    cart_product = [p for p in cart.objects.all() if p.user == user]

    if cart_product:
      for p in cart_product:
        tempamount = (p.quantity * p.product.discount_price)
        amount += tempamount
        totalamount = amount + shipping_amount
      return render(request,'app/addtocart.html',{'cartt':cartt, 'totalamount':totalamount, 'amount':amount})
    else:
      return render(request,'app/emptycart.html')

def plus_cart(request):
  if request.method == "GET":
    prod_id = request.GET['prod_id']
    c = cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity+=1
    c.save()
    amount = 0.0
    shipping_amount = 70.0
    cart_product = [p for p in cart.objects.all() if p.user == request.user]

    for p in cart_product:
      tempamount = p.quantity * p.product.discount_price
      amount += tempamount

    data ={
      'quantity':c.quantity,
      'amount':amount,
      'totalamount':amount + shipping_amount 
      }
    return JsonResponse(data)



def minus_cart(request):
  if request.method == "GET":
    prod_id = request.GET['prod_id']
    c = cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity-=1
    c.save()
    amount = 0.0
    shipping_amount = 70.0
    cart_product = [p for p in cart.objects.all() if p.user == request.user]

    for p in cart_product:
      tempamount = p.quantity * p.product.discount_price
      amount += tempamount  

    data ={
      'quantity':c.quantity,
      'amount':amount,
      'totalamount':amount + shipping_amount 
      }
    return JsonResponse(data)
  


def remove_cart(request):
  if request.method == "GET":
    prod_id = request.GET['prod_id']
    c = cart.objects.filter(Q(product=prod_id) & Q(user=request.user))
    c.delete()
    amount = 0.0
    shipping_amount = 70.0
    cart_product = [p for p in cart.objects.all() if p.user == request.user]

    for p in cart_product:
      tempamount = p.quantity * p.product.discount_price
      amount += tempamount    

    data ={
      'amount':amount,
      'totalamount':amount + shipping_amount 
      }
    return JsonResponse(data)



def buy_now(request):
  user = request.user
  add = Customer.objects.filter(user=user)
  cart_items = cart.objects.filter(user=user)
  amount = 0.0
  shipping_amount = 70.0
  totalamount = 0.0
  cart_product = [p for p in cart.objects.all() if p.user == request.user]

  if cart_product:
    for p in cart_product:
      tempamount =( p.quantity * p.product.discount_price)
      amount += tempamount 
    totalamount=amount + shipping_amount 
  return render(request, 'app/card.html',{'add':add, 'totalamount':totalamount, 'cart_items':cart_items})
  # return render(request, 'app/buynow.html')



@login_required
def profile(request):
 return render(request, 'app/profile.html')

@login_required
def address(request):
 add = Customer.objects.filter(user = request.user)
 return render(request, 'app/address.html', {'add':add, 'active':'btn-primary'})

@login_required
def orders(request):
  op = OrderPlaced.objects.filter(user=request.user)
  return render(request, 'app/orders.html',{'order_placed':op})

def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category = 'M')
    elif data == 'redmi' or data == 'samsung' or data== 'apple':
        mobiles = Product.objects.filter(category = 'M').filter(brand = data)
    elif data == 'below':
        mobiles = Product.objects.filter(category = 'M').filter(discount_price__lt=15000)
    elif data == 'above':
        mobiles = Product.objects.filter(category = 'M').filter(discount_price__gt=15000)
    return render(request, 'app/mobile.html',{'mobiles':mobiles})


def laptop(request, data=None):
    if data == None:
        laptops = Product.objects.filter(category = 'L')
    elif data == 'Asus' or data == 'Hp' or data== 'Apple' or data== 'Lenovo':
        laptops = Product.objects.filter(category = 'L').filter(brand = data)
    elif data == 'below':
        laptops = Product.objects.filter(category = 'L').filter(discount_price__lt=50000)
    elif data == 'above':
        laptops = Product.objects.filter(category = 'L').filter(discount_price__gt=50000)
    return render(request, 'app/laptop.html',{'laptops':laptops})



def topwear(request, data=None):
    if data == None:
        topwears = Product.objects.filter(category = 'TW')
    elif data == 'lp' or data == 'denim' or data== 'puma' or data== 'adidas' or data== 'usps':
        topwears = Product.objects.filter(category = 'TW').filter(brand = data)
    elif data == 'below':
        topwears = Product.objects.filter(category = 'TW').filter(discount_price__lt=500)
    elif data == 'above':
        topwears = Product.objects.filter(category = 'TW').filter(discount_price__gt=500)
    return render(request, 'app/topwear.html',{'topwears':topwears})

def bottomwear(request, data=None):
    if data == None:
      bottomwears = Product.objects.filter(category = 'BW')
    elif data == 'lp' or data == 'Denim' or data =='lee':
      bottomwears = Product.objects.filter(category = 'BW').filter(brand=data)
    elif data == 'below':
      bottomwears = Product.objects.filter(category = 'Bw').filter(discount_price__lt=500)
    elif data == 'above':
      bottomwears = Product.objects.filter(category = 'BW').filter(discount_price__gt=500)
    return render(request, 'app/bottomwear.html', {'bottomwears':bottomwears})

class CustomerRegistrationView(View):
  def get(self,request):
    form = CustomerRegistrationForm()
    return render(request, 'app/customerregistration.html', {'form':form})
  def post(self,request):
    form = CustomerRegistrationForm(request.POST)
    if form.is_valid():
      messages.success(request, "Congratulations! Registered Successfully")
      form.save()
    return render(request, 'app/customerregistration.html', {'form':form})
  
@login_required
def checkout(request):
  user = request.user
  add = Customer.objects.filter(user=user)
  cart_items = cart.objects.filter(user=user)
  amount = 0.0
  shipping_amount = 70.0
  totalamount = 0.0
  cart_product = [p for p in cart.objects.all() if p.user == request.user]

  if cart_product:
    for p in cart_product:
      tempamount =( p.quantity * p.product.discount_price)
      amount += tempamount 
    totalamount=amount + shipping_amount 
  return render(request, 'app/checkout.html',{'add':add, 'totalamount':totalamount, 'cart_items':cart_items})


@login_required
def payment_done(request):
  user = request.user
  custid = request.GET.get('custid')
  customer = Customer.objects.get(id=custid)
  cartt = cart.objects.filter(user=user)
  for c in cartt:
    OrderPlaced(user=user, customer=customer, product=c.product, quantity = c.quantity).save()
    c.delete()
  return redirect("orders")

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
  def get(self, request):
    form= CustomerProfileForm()
    return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})
  
  def post(self,request):
    form= CustomerProfileForm(request.POST)
    if form.is_valid():
      usr = request.user
      name = form.cleaned_data['name']
      locality = form.cleaned_data['locality']
      city = form.cleaned_data['city']
      zipcode = form.cleaned_data['zipcode']
      state = form.cleaned_data['state']
      reg = Customer(user=usr,name=name, locality=locality, city=city, zipcode=zipcode, state=state)
      reg.save()
      messages.success(request, 'Congratulatioin !! Your profile hass been update successfully')
    return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})