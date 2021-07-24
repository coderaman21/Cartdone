from typing import NamedTuple
from django.contrib import messages
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from . models import Product,Contact,Order,order_update
from math import ceil
import json

# Create your views here.
def index(request):
    # product = Product.objects.all()
    allprods = []
    categories = Product.objects.values('category')
    categories = {item['category'] for item in categories}
    for cat in categories:
        product = Product.objects.filter(category = cat)
        n= len(product)
        nslides = n//4 + ceil(n/4-n//4)
        nslides = range(1,nslides)
        allprods.append([product,nslides])
    # allprods = [[product,nslides],[product,nslides]]
    return render(request,'shop/index.html',{'allprods':allprods})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name' , '')
        email = request.POST.get('email' , '')
        number = request.POST.get('number' , '')
        desc = request.POST.get('desc' , '')
        contacts = Contact(name= name, email = email, number =  number, desc = desc)
        contacts.save()
    return render(request,'shop/contact.html')

def productview(request, myid):
    product = Product.objects.filter(product_id = myid)
    return render(request,'shop/productview.html', {'product':product})

def checkout(request):
    if request.method =="POST":
        items_json = request.POST.get('itemsJson','')
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        number = request.POST.get('number','')
        address = request.POST.get('address','')
        city = request.POST.get('city_name','')
        state = request.POST.get('state_name','')
        zipcode = request.POST.get('zip_code','')
        
        orders = Order(items_json = items_json , name = name , email = email, number = number,address = address,city = city ,state = state , zip_code = zipcode)
        orders.save()
        # save order to order_update class 
        id = orders.order_id
        OrderUpdate = order_update(order_id = id ,update_desc =  'your order has been placed succesfully' , name =name)
        OrderUpdate.save()

        thank = True
        return render(request,'shop/thanks.html',{'thanks':thank,'id':id})
    return render(request,'shop/checkout.html')

def tracker(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id','')
        email = request.POST.get('email','')
        try:
            order = Order.objects.filter(order_id = order_id , email = email)

            if len(order)>0:
                updates=[]
                update = order_update.objects.filter(order_id = order_id)
                for item in update:
                    updates.append({'text':item.update_desc,'time':item.timestamp})
                response = json.dumps([updates, order[0].items_json ],default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as E:
            return HttpResponse('{}')

    return render(request,'shop/tracker.html')

def search(request):
    if request.method == 'GET':
        query = request.GET['searchquery'].lower()

        allprods = Product.objects.all()   #fetch all products  
        prod_list = []                     #empty list of all products

        catprods = allprods.filter(category = query)   #fetch products by categroy 
        if catprods:
            # serach product by category
            for catprod in catprods:
                prod_list.append(catprod)
        else:
            # serach product by name
            for product in allprods:
                name=product.product_name
                if query in name.lower():
                    prod_list.append(product)

        # check if we could find searched product or not 
        if prod_list and len(query)>3:
            params ={'prod_list':prod_list,'query':query , 'result':True}
        else:
            params = {'query':query ,'result':False}

    return render(request,'shop/search.html', params)


def about(request):
    return render(request,'shop/about.html' )
   
def handlesignin(request):
    if request.method =="POST":
        signinusername = request.POST.get('signinusername')
        signinpassword = request.POST['signinpassword']

        # authenticate the user
        user = authenticate(username=signinusername,password=signinpassword)

        if user is not None:
            login(request,user)
            messages.success(request,f'You are succesfully loged in as {signinusername} .')
            return redirect('shopHome')     # "shopHome is the name of /shop/ endpoint "
        else: 
            messages.error(request,"Couldn't login invalid credientails maybe")
            return redirect('shopHome')
    else:

        return HttpResponse('error 404')

def handlesignout(request):
    logout(request)
    messages.success(request,'Successfully logged out')
    return redirect('shopHome')

def handlesignup(request):
    if request.method =="POST":
        # get values of inputs
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        username = request.POST['username']
        phone = request.POST['phone']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        # checks for erroneous inputs
        if len(username)>10:
            messages.error(request,'username can only be of 10 characters')
            return redirect('shopHome')
            
        if not username.isalnum():
            messages.error(request,'username can contain only letters and numbers')
            return redirect('/shop/')
        
        if not pass1==pass2:
            messages.error(request,"passwords didn't match")
            return redirect('/shop/')


        # create the user 
        myuser = User.objects.create_user(username,email ,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request,'congrats you account has succesfully been created')


        return redirect('/shop/')
    else:

        return HttpResponse('error 404')
