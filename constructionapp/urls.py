from django.urls import path, include
from django.conf.urls import url
from . import views
from django.conf import settings
from django.http import HttpResponseRedirect
from django.conf.urls.static import static

urlpatterns=[
    path('register/',views.registerPage, name = 'register'),
    path('login/',views.loginPage, name = 'login'),
    path('logout/',views.logoutUser, name = 'logout'),
    path('',views.home, name = 'home'),
    path('cart/',views.cart, name = 'cart'),
    path('checkout/',views.checkout, name = 'checkout'),
    path('update_item/',views.updateItem, name = 'update_item'),
    path('item_details/', views.details, name='details'),
    path('search/', views.search_products, name='search_products'),
    # url(r'^add-to-cart/(?P<item_id>[-\w]+)/$', views.add_to_cart, name="add_to_cart"),

]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)