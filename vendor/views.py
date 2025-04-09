from django.shortcuts import get_object_or_404, render, redirect
from accounts.forms import UserProfileForm
from vendor.models import Vendor, OpeningHour
from accounts.models import UserProfile
from vendor.forms import VendorForm, OpeningHourForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor
from menu.models import Category, FoodItem
from menu.forms import CategoryForm, FoodItemForm
from django.template.defaultfilters import slugify
from django.http import HttpResponse

def get_vendor(request):

    vendor = Vendor.objects.get(user=request.user)
    return vendor


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.add_message(request, messages.SUCCESS, "Settings updated!")
            return redirect('vprofile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)
    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor
    }
    return render(request, 'vendor/vprofile.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):

    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
    context = {
        'categories': categories
    }
    return render(request, 'vendor/menu_builder.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def food_items_by_category(request, pk=None):

    vendor = get_vendor(request)
    category = Category.objects.get(id=pk)
    food_items = FoodItem.objects.filter(category=category)

    context = {
        'category': category,
        'food_items': food_items,
    }
    return render(request, 'vendor/fooditems_by_category.html', context)
    

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.save()
            category.slug = slugify(category_name)+"-"+str(category.id)
            category.save()
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Category added successfully!')
            return redirect('menu_builder')
    else:
        form = CategoryForm()

    context = {
        'form': form,
    }
    return render(request, 'vendor/add_category.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request, pk=None):

    category = Category.objects.get(id=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Category updated successfully!')
            return redirect('menu_builder')
    else:
        form = CategoryForm(instance=category)

    context = {
        'form': form,
        'cat': category
    }
    return render(request, 'vendor/edit_category.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.add_message(request, messages.SUCCESS, "Category got deleted successfully.")
    return redirect('menu_builder')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_food(request):

    vendor = get_vendor(request)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES, vendor=vendor)
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = vendor
            food.save()
            food.slug = slugify(food_title)+"-"+str(food.id)
            food.save()
            messages.add_message(request, messages.SUCCESS, 'FoodItem added successfully!')
            return redirect('food_items_by_category', food.category.id)
    else:
        form = FoodItemForm(vendor=vendor)

    context = {
        'form': form,
    }
    return render(request, 'vendor/add_food.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_food(request, pk=None):

    food = FoodItem.objects.get(id=pk)
    vendor = get_vendor(request)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES, instance=food)
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = vendor
            food.save()
            food.slug = slugify(food_title)+"-"+str(food.id)
            food.save()
            messages.add_message(request, messages.SUCCESS, 'FoodItem updated successfully!')
            return redirect('food_items_by_category', food.category.id)
    else:
        form = FoodItemForm(vendor=vendor, instance=food)

    context = {
        'form': form,
        'food': food
    }
    return render(request, 'vendor/edit_food.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_food(request, pk=None):
    food = get_object_or_404(FoodItem, pk=pk)
    food.delete()
    messages.add_message(request, messages.SUCCESS, "FoodItem got deleted successfully.")
    return redirect('food_items_by_category', food.category.id)

def opening_hours(request):
    opening_hours = OpeningHour.objects.filter(vendor=get_vendor(request))
    forms = OpeningHourForm()
    context = {
        'form': forms,
        'opening_hours': opening_hours,
    }

    return render(request, 'vendor/opening_hours.html', context)

def add_opening_hours(request):

    if request.uset.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
            day = request.POST.get('hour')
            from_hour = request.POST.get('from_hour')
            to_hour = request.POST.get('to_hour')
            is_closed = request.POST.get('is_closed')
        
        try:
            hour = OpeningHour.objects.create(vendor=get_vendor(requet), day=day, from_hour=from_hour, to_hour=to_hour, is_closed=is_closed)
            response = {'status': 'success'}
            return JsonResponse(response)

        except IntegrityError as e:
            response = {'status': 'failed'}
            return JsonResponse(response)
            
    return HttpResponse('Add opening hour')