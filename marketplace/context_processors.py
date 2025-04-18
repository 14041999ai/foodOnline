from .models import Cart, Tax
from menu.models import FoodItem


def get_cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            if cart_items:
                for cart_item in cart_items:
                    cart_count += cart_item.quantity
            else:
                cart_count = 0
        except:
            cart_count = 0
    return dict(cart_count=cart_count)


def get_cart_amounts(request):
    subtotal = 0
    tax = 0
    grand_total = 0

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            food_id = item.fooditem.id
            food_item = FoodItem.objects.get(pk=food_id)
            subtotal += (item.quantity*food_item.price)
        get_tax = Tax.objects.filter(is_active=True)
        grand_total = subtotal+tax
    return dict(subtotal=subtotal, tax=tax, grand_total=grand_total)

