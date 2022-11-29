from django.shortcuts import render,redirect
from store.models import Product
from django.contrib import auth
from django.contrib import messages


def home(request):
    
    products = Product.objects.all().filter(is_avilable= True)
    future_product = Product.objects.all().filter(is_featured = True, is_avilable =True)
    today_offer    = Product.objects.all().filter(today_offer = True, is_avilable = True)
    shoes_pair = Product.objects.all().filter(shoes_pair= True, is_avilable= True)

    context ={
        'products':products,
        'f_product' :future_product,
        'today_offer' :today_offer,
        'shoes_pair' : shoes_pair
    }
    return render(request,'index.html', context)



def admin_login(request):
    if request.method =="POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user    = auth.authenticate(email=email , password=password)
        if user is not None:
            if user.is_superadmin: 
                auth.login(request,user)
                return redirect('adminpanel')
            else:
                messages.info(request,'user is not superuser')
                return redirect('admin_login')
        else:
            messages.info(request,'Please enter valid username or password')
            return redirect('admin_login')
    return render(request,'adminpanel/adminlogin.html')

