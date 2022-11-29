from email.message import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from. models import Account,UserProfile
from accounts.form import RegistrationForm, UserForm,UserProfileForm
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from carts.views import _cart_id
from carts.models import Cart, CartItem
from django.contrib.auth import login
import requests
from orders.models import Order
from .models import Messages
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name  = form.cleaned_data['last_name']
            email      = form.cleaned_data['email']
            password   = form.cleaned_data['password']
            username   = email.split("@")[0]
            user = Account.objects.create_user(first_name= first_name, last_name = last_name, email= email,username= username, password = password)
            user.save()
            # user activation
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_varification_email.html',{
                'user' : user,
                'domain' :current_site,
                'uid'  : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' :default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request,'Verify your e-mail to finish signing up for s-box')
            return  redirect('login')
        
    else:
        form = RegistrationForm()
    context = {
        'form' : form
    }
    return render(request,'accounts/register.html',context)


def activate(request, uidb64, token):
    try :
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError,Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,'Congratulation! your account is activated')
        return redirect('login')
    else:
        messages.error(request,'Invalid activation link')
        return redirect('register')



def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user    = auth.authenticate(email=email , password=password)
        if user is not None:
                try:
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                    is_cart_item_exists = Cart_item.objects.filter(cart=cart).exists()
                    if is_cart_item_exists:
                        cart_item = Cart_item.objects.filter(cart=cart)


                        #getting product variation by cart id
                        product_variation = []
                        for item in cart_item:
                            variation = item.variations.all()
                            product_variation.append(list(variation))

                        #getting user's product variations
                        cart_item = Cart_item.objects.filter(user=users)
                        existing_variation_list = []
                        id = []
                        print(cart_item)
                        print(existing_variation_list)
                        for item in cart_item:
                            existing_variation = item.variations.all()
                            existing_variation_list.append(list(existing_variation))
                            id.append(item.id)

                        for product_variation_item in product_variation:
                            if product_variation_item in existing_variation_list:
                                index = existing_variation_list.index(product_variation_item)
                                item_id = id[index]
                                item = Cart_item.objects.get(id=item_id)
                                item.quantity += 1
                                item.user = users
                                item.save()
                            else:
                                cart_item = Cart_item.objects.filter(cart=cart)
                                for item in cart_item:
                                    item.user = users
                                    item.save()
                except:
                    pass
                login(request,user)
                url = request.META.get('HTTP_REFERER')
                try:
                    query = requests.utils.urlparse(url).query
                    params = dict(value.split('=') for value in query.split('&'))
                    print(params)
                    if 'next' in params:
                        next_page = params['next']
                        return redirect(next_page)
                except:
                    return redirect('home')
        else:
            messages.error(request,'Enter a valid username and password')
        
    return render(request,'accounts/login.html')


@login_required(login_url = 'login')
def user_logout(request):
    auth.logout(request)
    messages.success(request,'You are logged out')
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id = request.user.id, is_ordered=True)
    orders_count = orders.count()
    UserProfile.objects.get_or_create(user=request.user)
    userprofile = UserProfile.objects.get(user=request.user)
    context = {
        'orders_count' :orders_count,
        'userprofile'  :userprofile,
    }
    return render(request,'accounts/dashboard.html',context)


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email = email).exists():
            user = Account.objects.get(email__exact=email)
            current_site = get_current_site(request)
            mail_subject = 'Reset your password'
            message = render_to_string('accounts/reset_password_email.html',{
                'user' : user,
                'domain' :current_site,
                'uid'  : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' :default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request,'password reset email has been sent to your email address')
            return redirect('login')
        else :
            messages.error(request,'Accout does not exist')
            return redirect('forgotPassword')


    return render(request,'accounts/forgotPassword.html')

def resetpassword_validate(request, uidb64, token):
    try :
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError,Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        return redirect('resetPassword')
    else:
        messages.error(request, 'This is link has been expired')
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk = uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset done successful')
            return redirect('login')
        
        else:
            messages.error(request,'Password do not match')
            return redirect('resetPassword')
    else:
        return render(request,'accounts/resetPassword.html')


@login_required(login_url= 'login')
def my_orders(request):
    orders = Order.objects.filter(user= request.user, is_ordered = True).order_by('-created_at')
    context ={
        'orders' :orders
    }
    return render(request,'accounts/my_orders.html', context)



@login_required(login_url= 'login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user = request.user)
    if request.method =='POST':
        user_form = UserForm(request.POST, instance= request.user)
        profile_form = UserProfileForm(request.POST,request.FILES,instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Your profile has been updated')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form' : user_form,
        'profile_form' :profile_form,  
        'userprofile'   : userprofile # for profile picture
    }
    return render(request, 'accounts/edit_profile.html',context)

@login_required(login_url= 'login')
def change_password(request):
    if request.method == 'POST':
         current_password = request.POST['current_password']
         new_password = request.POST['new_password']
         confirm_password = request.POST['confirm_password']

         user = Account.objects.get(first_name__exact = request.user.first_name)
         

         if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request,'password updated successfully')
                return redirect('change_password')
            else:
                messages.error(request, 'Please enter valid current passowrd')
                return redirect('change_password')
         else:
             messages.error(request, 'Password does not mathch!')
             return redirect('change_password')
        
    return render(request,'accounts/change_password.html')


def contact(request):
    if request.method == "POST":
        contact = Messages()
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('massage')
        contact.name = name
        contact.email = email
        contact.subject = subject
        contact.save()
        messages.success(request,'Your  messages submitted successfully')
        return redirect('home')


def contactpage(request):
    return render(request,'contact.html')