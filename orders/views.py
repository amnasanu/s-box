import datetime
from django.shortcuts import redirect, render
from django.http import JsonResponse
from accounts.models import Account
from carts.models import CartItem
from .forms import OrderForm
from .models import Order, OrderProduct, Payment
import json
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import razorpay
from django.conf import settings
from .models import Profile
from django.contrib import messages
# Create your views here.


def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False,order_number=body['order_id'])

    # store transaction details inside Payment model
    payment = Payment(
        user = request.user,
        payment_id = body['razorpay_payment_id'],
        payment_method = body['payment_method'],
        amount_paid = body['amount_paid'],
        status = body['status'],
        payment_signature = body['razorpay_signature'],
        razorpay_order_id = body['razorpay_order_id']
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # move the cart items to Order product table
    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id = item.id) 
        product_variation= cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variation.set(product_variation)
        orderproduct.save()

        # reduce the quantity of the sold products
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()
    # clear cart
    CartItem.objects.filter(user = request.user).delete()

    #send order recive email to costomer
    mail_subject = 'Thank you for your order'
    message = render_to_string('orders/order_recieved_email.html',{
        'user' : request.user,
        'order' : order,
        })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()
    
    # Send order number and transation id back to sendData method via JavaResponse

    data = {
        'order_number' : order.order_number,
        'transID'      : payment.payment_id,
    }

    return JsonResponse(data)

def place_order(request, total = 0, quantity = 0):
    current_user = request.user
    # if the cart count is less han or equal to 0 then redirect bak to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <=0:
        return redirect('store')
    grandtotal = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2*total)/100
    
    grandtotal = total+tax

    if request.method =='POST':

        if not Profile.objects.filter(user = request.user.id):
            userprofile = Profile()
            userprofile.user = request.user
            userprofile.phone  = request.POST.get('phone')
            userprofile.address_line_1 = request.POST.get('address_line_1')
            userprofile.address_line_2 = request.POST.get('address_line_2')
            userprofile.city = request.POST.get('city')
            userprofile.state = request.POST.get('state')
            userprofile.country = request.POST.get('country')
            userprofile.save()

        form =  OrderForm(request.POST)
        if form.is_valid():
            #store the billing information inside the order table
            data= Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.email = form.cleaned_data['email']
            data.phone  = form.cleaned_data['phone']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.city = form.cleaned_data['city']
            data.state = form.cleaned_data['state']
            data.country = form.cleaned_data['country']
            data.order_note = form.cleaned_data['order_note']
            data.order_total =grandtotal
            data.tax =  tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            #Generate order number
            yr = int(datetime.date.today().strftime('%y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered =False, order_number= order_number)
            client = razorpay.Client(auth=(settings.KEY , settings.SECRET))
            DATA = {
                "amount" : int(data.order_total),
                "currency" : "INR",
                "payment_capture" : 1,
            }
            payment = client.order.create(data=DATA)
            print(order_number)
            print("*************")
            print(payment)
            print("*************")

            context = {
                'order' : order, 
                'cart_items' :cart_items,
                'total' : total,
                'tax' : tax,
                'grand_total' :grandtotal,
                'payment' : payment
            }
            return render(request,'orders/payments.html', context)
        else:
            messages.error(request,'Fill the form')
            return redirect('place_order')
    else:
        return redirect('checkout')


def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)

        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        payment = Payment.objects.get(payment_id = transID)
        order_sub_total = order.order_total - order.tax
        context = {
            'order' : order,
            'order_number' : order.order_number,
            'transID' : payment.payment_id,
            'payment' : payment,
            'ordered_products': ordered_products,
            'order_sub_total':order_sub_total,
        }

        return render(request,'orders/order_complete.html',context)   
    except(Payment.DoesNotExist, Order.DoesNotExist):
        return redirect ('home')


def order_cancel(request,order_id):
    order=Order.objects.get(id=order_id)
    order.status = 'Cancelled'
    order.save()
    return redirect('my_orders')