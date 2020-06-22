from django.shortcuts import render,redirect
from .forms import CreateUserForm,UserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from .models import *
import json
import datetime
from django.http import JsonResponse

# Create your views here.

def IndexView(request):
    
    return render(request,'index.html')
@login_required(login_url="notloggedin")
def RestaurantView(request):
    customer=request.user.customer
    order=Order.objects.filter(customer=customer,completed=False)
    print(order)
    if order is not None:
        order.delete()   
    restuarants=Restaurant.objects.all()    
    context={"restuarants":restuarants}
    return render(request,'individual_restaurant.html',context)    

def IndividualView(request,id):
    restaurant=Restaurant.objects.get(id=id)
    products=Product.objects.filter(restaurant_id=id)
    context={'products':products,'restaurant':restaurant} 
    return render(request,'restaurants.html',context)       

def NotLoggedInView(request):
    return render(request,'notLoggedIn.html')    

@login_required(login_url="notloggedin")
def CartView(request):
    customer=request.user.customer
    order,created=Order.objects.get_or_create(customer=customer,completed=False)
    items=order.orderitems_set.all()
    total=order.get_cart_items
    

    context={"order":order,"items":items,"total":total}
    return render(request,'cart.html',context)

@login_required(login_url="notloggedin")
def CheckoutView(request):
    customer=request.user.customer
    order,created=Order.objects.get_or_create(customer=customer,completed=False)
    items=order.orderitems_set.all()
    total=order.get_cart_items
    

    context={"order":order,"items":items,"total":total}
    return render(request,'checkout.html',context)    


def RegisterView(request):
    form=CreateUserForm()
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            Customer.objects.create(
                user=user,
                name=user.username,
                email=user.email
            )
            username=form.cleaned_data.get('username')
            messages.success(request,'Account created for'+username)
            return redirect('login')
        print(form.errors)
    context={'form':form}        
    return render(request,'register.html',context)    



def LoginView(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        messages.info(request,'Incorrect Username or Password')

    return render(request,'login.html') 

def LogoutView(request):
    logout(request)
    return redirect('home')               

def UpdateOrder(request):
    data=json.loads(request.body)
    productId=data['productId']
    action=data['action']
    print(productId,action)
    customer=request.user.customer
    product=Product.objects.get(id=productId)
    order,created=Order.objects.get_or_create(customer=customer,completed=False)
    orderItem,created=OrderItems.objects.get_or_create(order=order,product=product)

    if action=="add":
        orderItem.quantity=orderItem.quantity+1
    elif action=="remove":
        orderItem.quantity=orderItem.quantity-1
    orderItem.save()
    
    if orderItem.quantity<=0:
        orderItem.delete()
    print(Order.objects.all())
    return JsonResponse('Item was added',safe=False)

def ProcessOrder(request):
    transaction_id=datetime.datetime.now().timestamp()
    data=json.loads(request.body)

    if request.user.is_authenticated:
        customer=request.user.customer
        order,created= Order.objects.get_or_create(customer=customer,completed=False)
        total=float(data['shipping']['total'])
        order.transaction_id=transaction_id
        if total==order.get_cart_total:
            order.completed=True
        order.save()
        
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode']

            )    
    else:
        print('User not logged in')    
    return JsonResponse('Payment Complete',safe=False)    



def UserAccountsView(request):
    profile=request.user.customer
    
    order=Order.objects.filter(customer=profile,completed=True)
    
    form=UserForm(instance=profile)
    if request.method=="POST":
        form=UserForm(request.POST,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_accounts')    
    context={"form":form,"orders":order}
    return render(request,'useraccount.html',context)  

def OrderSummaryView(request,pk):
    customer=request.user.customer
    order=Order.objects.get(id=pk)
    items=order.orderitems_set.all()
    total=order.get_cart_items
    context={"items":items,"total":total,"order":order}
    return render(request,'ordersummary.html',context)     