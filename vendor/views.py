from django.shortcuts import get_object_or_404, render
from accounts.forms import UserProfileForm
from vendor.models import Vendor
from accounts.models import UserProfile
from vendor.forms import VendorForm


def vprofile(request):

    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    profile_form = UserProfileForm(instance=profile)
    vendor_form = VendorForm(instance=vendor)
    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor
    }
    return render(request, 'vendor/vprofile.html', context)
