from django.shortcuts import render, redirect
from marketplace.models import Cart
from marketplace.context_processors import get_cart_amounts
from .forms import OrderForm
from .models import Order
import simplejson as json
from .utils import generate_order_number

def place_order(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace')

    subtotal = get_cart_amounts(request)['subtotal']
    total_tax = get_cart_amounts(request)['tax']
    grand_total = get_cart_amounts(request)['grand_total']
    tax_data = get_cart_amounts(request)['grand_total']

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order.pin_code = form.cleaned_data['pin_code']
            order.user = request.user
            order.total = grand_total
            order.total_tax = total_tax
            order.tax_data = json.dumps(tax_data)
            order.payment_method = request.POST['payment_method']
            order.save()
            order.order_number = generate_order_number(order.id)
            order.save()
        else:
            print(form.errors)

    return render(request, 'orders/place_order.html')

def payments(request):
    # check if request is ajax or not
    if request.headers.get('x-requested-with')=='XMLHttpRequest' and request.method == 'POST':

    # STORE THE PAYMENT DETAILS IN THE PAYMENT MODEL
        order_number = request.POST.get('order_number')
        transaction_id = request.POST.get('transaction_id')
        payment_method = request.POST.get('payment_method')
        status = request.POST.get('status')

        order = Order.objects.get(user=request.user, order_number=order_number)
        payment = Payment(
            user = request.user,
            transaction_id = transaction_id,
            payment_method = payment_method,
            amount = order.total,
            status = status
        )
        payment.save()

        # UPDATE THE ORDER MODEL
        order.payment = payment
        order.is_ordered = True
        order.save()
        return HttpResponse('Saved!')
        # MOVE THE CART ITEMS TO ORDERED FOOD MODEL

        # SEND ORDER CONFIRMATION EMAIL TO THE CUSTOMER

        # SEND ORDER RECIEVED EMAIL TO VENDOR

        # CLEAR THE CART IF PAYMENT IS SUCCESS

        # RETURN BACK TO AJAX WITH THE STATUS SUCCESS OR FAILURE

    return HttpResponse("Payment view")