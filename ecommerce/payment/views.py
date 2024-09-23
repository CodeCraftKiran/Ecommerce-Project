from django.shortcuts import render
from . models import ShippingAddress, Order, OrderItem
from cart.cart import Cart
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

def checkout(request):
    # Users with accounts -- Pre-fill the form
    if request.user.is_authenticated:
        try:
            # Authenticated users WITH shipping information
            shipping_address = ShippingAddress.objects.get(user=request.user.id)
            context = {'shipping': shipping_address}
            return render(request, 'payment/checkout.html', context=context)
        except:
            # Authenticated user with No shipping information.
            return render(request, 'payment/checkout.html')
    else:
        # Guest Users
        return render(request, 'payment/checkout.html')



def complete_order(request):
   if request.POST.get('action') == 'post':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        
        # All-in-one shipping address
        shipping_address = (address1 + '\n' + address2 + '\n' +
                            city + '\n' + state + '\n' + zipcode)

        # Shopping cart information
        cart = Cart(request)
        
        # Get the total price of items
        total_cost = cart.get_total()
        
        
        """
        order variations
        1) Create order -> Account user WITH + WITHOUT shipping information
        2) create order -> Guest users without an account
        """
        
        # 1) Create order -> Account user WITH + WITHOUT shipping information    
        if request.user.is_authenticated:
            order = Order.objects.create(full_name=name, email=email, shipping_address=shipping_address, amount_paid=total_cost, user=request.user)
            order_id = order.pk
            
            product_list = []
            for item in cart:
                OrderItem.objects.create(order_id=order_id, product=item['product'], quantity=item['qty'], price=item['price'], user=request.user)
                product_list.append(item['product'])

            all_products = product_list

            # Email order verification
            send_mail(
                subject='Order received',
                message=(
                    'Hi,\n\n'
                    'Thank you for placing your order.\n\n'
                    'Please see your order below:\n\n'
                    f'{str(all_products)}\n\n'
                    f'Total Paid: {str(cart.get_total())}'
                ),
                from_email=settings.EMAIL_HOST_USER,
                recipient=[email],
                fail_silently=False,
            )
        
        
        # 2) create order -> Guest users without an account
        else:
            order = Order.objects.create(full_name=name, email=email, shipping_address=shipping_address, amount_paid=total_cost)
            order_id = order.pk
            
            product_list = []
                
            for item in cart:
                OrderItem.objects.create(order_id=order_id, product=item['product'], quantity=item['qty'], price=item['price'])
                product_list.append(item['product'])

            all_products = product_list
            
            
        # Email order verification
        send_mail('Order received', 'Hi ' + '\n\n' + 'Thank you for placing your order.'+ '\n\n' +
                'please see your order below' + '\n\n' + str(all_products) + '\n\n' + 'Total Paid: ' + str(cart.get_total()),
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
                )
        
        order_success = True
        response = JsonResponse({'success': order_success})
        return response    



def payment_success(request):
    # Clear shopping cart
    for key in list(request.session.keys()):
        if key == 'session_key':
            del request.session[key]
    return render(request, 'payment/payment-success.html')



def payment_failed(request):
    return render(request, 'payment/payment-failed.html')