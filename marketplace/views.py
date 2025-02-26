from django.http import HttpResponse
from django.shortcuts import render
from vendor.models import Vendor
from menu.models import Category, FoodItem
from django.db.models import Prefetch


def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count
    }
    return render(request, 'marketplace/listings.html', context)

def vendor_detail(request, vendor_slug):
    vendor = Vendor.objects.get(slug=vendor_slug)
    available_fooditems = FoodItem.objects.filter(is_available=True)
    prefetch = Prefetch("fooditems", queryset=available_fooditems)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(prefetch)

    context = {
        "vendor": vendor,
        "categories": categories
    }
    return render(request, 'marketplace/vendor_detail.html', context)

def add_to_cart(request, food_id):
    return HttpResponse(food_id)
