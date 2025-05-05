from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from marketplace import views as marketplace_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('', include('accounts.urls')),
    path('marketplace/', include('marketplace.urls')),
    #CART
    path('cart/', marketplace_views.cart, name="cart"),
    # SEARCH
    path('search/', marketplace_views.search, name='search'),
    path('checkout/', marketplace_views.checkout, name='checkout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
