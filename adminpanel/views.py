from category.forms import CategoryForm
from django.contrib import messages
from django.shortcuts import redirect, render
from accounts.models import Account
from carts.models import Cart,CartItem
from category.models import Category
from orders.models import Order, OrderProduct, Payment
from store.models import  Product,  Variation
from django.template.defaultfilters import slugify
from django.db.models import Sum
from django.contrib.auth.decorators import login_required 
from django.db.models.functions import TruncMinute
import datetime
from store.forms import VariationForm
from store.models import ProductGallery
from store.forms import ProductForm
from django.db.models import Q
from django.contrib import auth
from django.core.paginator import Paginator
from django.contrib import messages
from accounts.models import Messages


# Create your views here.

@login_required(login_url="login")
def user_accounts_table(request,id):
    if request.user.is_superadmin:
        active_users = Account.objects.all().filter(is_admin=False,is_active=True)
        banned_users = Account.objects.all().filter(is_admin = False, is_active =False)
        context  = {
            'active_users' : active_users,
            'banned_users' : banned_users,
        }
        if id==1:
            return render(request,'adminpanel/admin_accounts/active_users.html',context)
        else:
            return render(request,'adminpanel/admin_accounts/banned_users.html',context)
    else:
        return redirect ('home')


@login_required(login_url="login")
def ban_user(request,id):
    if request.user.is_superadmin:
        user           = Account.objects.get(id=id)
        user.is_active = False
        user.save()
        return redirect('user_accounts_table',id=1)
    else:
        return redirect ('home')


@login_required(login_url="login")
def unban_user(request,id):
    if request.user.is_superadmin:
        user           = Account.objects.get(id=id)
        user.is_active = True
        user.save()
        return redirect('user_accounts_table',id=2)
    else:
        return redirect ('home')
    
@login_required(login_url="login")
def cart_table(request,id):
    if request.user.is_superadmin:
        carts = Cart.objects.all()
        cart_items = CartItem.objects.all().filter(is_active =True)
        context = {
            'carts' : carts,
            'cart_items' : cart_items,
        }
        if id==1:
            return render(request,'adminpanel/cart_table/cart.html',context)
        else:
            return render(request,'adminpanel/cart_table/cart_items.html',context)
    else:
        return redirect ('home')

@login_required(login_url="login")
def category_table(request,id):
    if request.user.is_superadmin:
        category = Category.objects.all()
        context = {
            'category' : category,
        }
        if id==2:
            return render(request,'adminpanel/category_table/category.html',context)
        else:
            return render(request,'adminpanel/category_table/sub_category.html',context)
    else:
        return redirect ('home')

# main category



@login_required(login_url="login")
def add_category(request):
    if request.user.is_superadmin:
        form = CategoryForm()
        if request.method == 'POST':
            form = CategoryForm(request.POST)
            if form.is_valid():
                category = form.save()
                category_name = form.cleaned_data['category_name']
                slug = slugify(category_name)
                category.slug = slug
                category.save()
                messages.success(request,'New category added successfully')
                return redirect('category_table',id=2)
            else:
                messages.success(request,'Category already exists')
                return redirect('add_category')
            
        context = {
            'form' : form,
        }
        return render (request,'adminpanel/category_table/add_category.html',context)
    else:
        return redirect('home')

@login_required(login_url="login")
def edit_category(request,id):
    if request.user.is_superadmin:
        category = Category.objects.get(id=id)
        if request.method == 'POST':
            form = CategoryForm(request.POST, instance=category)
            if form.is_valid():
                category_name = form.cleaned_data['category_name']
                slug = slugify(category_name)
                category = form.save()
                category.slug = slug
                category.save()
                messages.success(request,'category editted successfully')
                return redirect('category_table',id=2)
            else:
                messages.info(request,'category already exists')
        else:
            form = CategoryForm(instance=category)
        context = {
            'form' : form,
        }
        return render (request,'adminpanel/category_table/add_category.html',context)
    else:
        return redirect('home')


@login_required(login_url="login")
def delete_category(request,id):
    if request.user.is_superadmin:
        category = Category.objects.get(id=id)
        category.delete()
        messages.success(request,'Category deleted successfully')
        return redirect ('category_table',id=2)
    else:
        return redirect ('home')

# category end

# sub Category star



       
@login_required(login_url="login")
def order_table(request,id):
    if request.user.is_superadmin:
        orders = Order.objects.filter(is_ordered=True,status='New')
        accepted_orders = Order.objects.filter(is_ordered=True,status='Accepted')
        completed_orders = Order.objects.filter(is_ordered=True,status="Delivered")
        cancelled_orders = Order.objects.filter(is_ordered=True,status="Cancelled")
        order_products = OrderProduct.objects.all()
        payments = Payment.objects.all()
        context = {
            'orders' : orders,
            'order_products' : order_products,
            'payments' : payments,
            'accepted_orders' : accepted_orders,
            'completed_orders' : completed_orders,
            'cancelled_orders' : cancelled_orders,
        }

        if id==1:
            return render (request,'adminpanel/order_table/orders.html',context)
        elif id==2:
            return render(request,'adminpanel/order_table/accepted_orders.html',context)
        elif id==3:
            return render(request,'adminpanel/order_table/completed_orders.html',context)
        elif id==4:
            return render(request,'adminpanel/order_table/cancelled_orders.html',context)
        else:
            return render(request,'adminpanel/order_table/payments.html',context)
    else:
        return redirect('home')


@login_required(login_url="login")
def order_accepted(request,order_id):
    if request.user.is_superadmin:
        order = Order.objects.get(id=order_id)
        order.status = 'Accepted'
        order.save()
        return redirect('order_table',id=1)
    else:
        return redirect ('home')


@login_required(login_url="login")
def order_completed(request,order_id):
    if request.user.is_superadmin:
        order=Order.objects.get(id=order_id)
        order.status = 'Delivered'
        order.save()
        return redirect('order_table',id=2)
    else:
        return redirect('home')


@login_required(login_url="login")
def order_cancelled(request,order_id):
    if request.user.is_superadmin:
        order=Order.objects.get(id=order_id)
        order.status = 'Cancelled'
        order.save()
        return redirect('order_table',id=1 )
    else:
        return render(request,'adminpanel/order_table/order_cancelled.html')




@login_required(login_url="login")
def store_table(request,id):
    if request.user.is_superadmin:
        products = Product.objects.all()
        variations =Variation.objects.all()

        context = {
            'products' : products,
            'variations' : variations,
        }
        if id==1:
            return render(request,'adminpanel/store_table/products.html',context)
        else:
            return render(request,'adminpanel/store_table/variations.html',context)
    else:
        return redirect('home')


@login_required(login_url="login")
def add_product(request):
    if request.user.is_superadmin:
        form = ProductForm()
        if request.method == 'POST':
            form = ProductForm(request.POST,request.FILES)
            if form.is_valid():
                if form.cleaned_data['price'] >= 50 :
                    product = form.save(commit=False)
                    product_name = form.cleaned_data['product_name']
                    slug = slugify(product_name)
                    product.slug = slug
                    product.save()
                    # images = request.FILES.getlist('images')
                    # for image in images:
                    #     ProductGallery.objects.create(
                    #         image = image,
                    #         product = product,
                    #     )
                    return redirect('store_table',id=1)
                else:
                    messages.info(request,'Please make price atleast Rs 50')
                    
            else:
                messages.info(request,'Product already exists')
        else:
            form = ProductForm()
        context = {
            'form' : form,
        }
        return render(request,'adminpanel/store_table/add_product.html',context)
    else:
        return redirect('home')

@login_required(login_url="login")
def edit_product(request,id):
    if request.user.is_superadmin:
        product = Product.objects.get(id=id)
        more_images = ProductGallery.objects.filter(product=product)
        if request.method =='POST':
            form = ProductForm(request.POST,request.FILES,instance=product)
            if form.is_valid():
                product_name = form.cleaned_data['product_name']
                slug = slugify(product_name)
                product = form.save()
                product.product_slug = slug
                product.save()

                images = request.FILES.getlist('images')
                for image in images:
                    ProductGallery.objects.create(
                        image = image,
                        product = product,
                    )
                
                return redirect('store_table',id=1)
            else:
                messages.info(request,'product already exists')
        else:
            form = ProductForm(instance=product)
        context = {
            'form' : form,
            'more_images' :more_images,

        }
        return render (request,'adminpanel/store_table/add_product.html',context)
    else:
        return redirect ('home')


@login_required(login_url="login")
def delete_product(request,id):
    if request.user.is_superadmin:
        product = Product.objects.get(id=id)
        product.delete()
        return redirect('store_table',id=1)
    else:
        return redirect ('home')


@login_required(login_url="login")     
def add_variations(request):
    if request.user.is_superadmin:
        form = VariationForm()
        if request.method == 'POST':
            form = VariationForm(request.POST)
            print(form)
            if form.is_valid():
                if Variation.objects.filter(variation_value__startswith=Variation.variation_value).exists():
                    messages.info(request,"Variation already exists")
                    return redirect('add_variations')
                form.save()
                messages.info(request,"Your variation added successfully")
                return redirect('store_table',id=2)
            else:   
                messages.info(request,  'Variation is already exist')
                return redirect('add_variations')
        else:
            form = VariationForm()
        context = {
            'form' : form,
        }
        return render(request,'adminpanel/store_table/add_variations.html',context)
    else:
        return redirect('home')


@login_required(login_url="login")
def edit_variations(request,id):
    if request.user.is_superadmin:
        variation = Variation.objects.get(id=id)
        if request.method =='POST':
            form = VariationForm(request.POST,instance=variation)
            if form.is_valid():
                form.save()
                return redirect('store_table',id=2)
        else:
            form = VariationForm(instance=variation)
        context = {
            'form' : form,
        }
        return render (request,'adminpanel/store_table/add_variations.html',context)
    else:
        return redirect ('home')


@login_required(login_url="login")
def delete_variatons(request,id):
    if request.user.is_superadmin:
        variation = Variation.objects.get(id=id)
        variation.delete()
        return redirect('store_table',id=2)
    else:
        return redirect ('home')





@login_required(login_url="admin_login")
def adminpanel(request):
    messages = Messages.objects.all()
    if request.user.is_superadmin:
        total_revenue = round( Order.objects.filter(is_ordered = True).aggregate(sum = Sum('order_total'))['sum'])
        total_cost= round((total_revenue * .80))
        total_profit = round(total_revenue - total_cost)  
        chart_year = datetime.date.today().year
        chart_month = datetime.date.today().month

         #getting daily revenue
        daily_revenue = Order.objects.filter(                     
            created_at__year=chart_year,created_at__month=chart_month
        ).order_by('created_at').annotate(day=TruncMinute('created_at')).values('day').annotate(sum=Sum('order_total')).values('day','sum')

        day=[]
        revenue=[]
        for i in daily_revenue:
            day.append(i['day'].minute)
            revenue.append(int(i['sum']))
        product_count = OrderProduct.objects.all().count()

       
        context = {
            'total_revenue' : total_revenue,
            'total_cost' : total_cost,
            'total_profit' : total_profit,
            'product_count' : product_count,
            'day' : day,
            'revenue' : revenue,
            'message' : messages,
        }
        return render (request,'adminpanel/adminpanel.html',context)
    else:
         return redirect('admin_login')

def admin_logout(request):
    auth.logout(request)
    messages.success(request,'You are logged out')
    return redirect('admin_login')




def todayoffer(request):
    today_offer    = Product.objects.all().filter(today_offer = True, is_avilable = True)
    product = Product.objects.all().filter(is_avilable = True)
    context = {
        'today_offer' : today_offer,
        'product': product,
        
    }
    return render(request,'adminpanel/todayoffer.html', context)


def changetodayoffer(request):
    if request.method == "POST":
        product = request.POST.get('product')
        print(product)
        pro = Product.objects.get(product_name = product)
        pro.today_offer = True
        pro.save()
        return redirect('today_offer')


    