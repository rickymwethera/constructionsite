from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import *
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CreateUserForm
from .utils import cookieCart, cartData
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('/')

    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

    context = {'form':form}
    return render(request, 'accounts/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')

        else:
            messages.info(request, 'Username or Password is incorrect')
            


    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    items_list = Product.objects.all()
    category = Category.get_category()
    return render (request, 'home.html', {'items_list':items_list, 'cartItems':cartItems})

def cart(request):

    if request.user.is_authenticated:
        profile = request.user.profile
        order, created = Order.objects.get_or_create(profile=profile, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        
    context = {'items':items, 'order':order}
    return render(request, 'cart.html', context)

def checkout(request):

    if request.user.is_authenticated:
        profile = request.user.profile
        order, created = Order.objects.get_or_create(profile=profile, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        
    context = {'items':items, 'order':order}
    return render(request, 'checkout.html', context)
    

def search_products(request):
    categorys = Category.get_category()
    filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=False)
    current_order_products = []
    if filtered_orders.exists():
    	user_order = filtered_orders[0]
    	user_order_items = user_order.items.all()
    	current_order_products = [product.product for product in user_order_items]

    if 'searchproduct' in request.GET and request.GET["searchproduct"]:
        search_term = request.GET.get("searchproduct")
        searched_project = Product.search_by_name(search_term)
        message = f"{search_term}"
        context = {'object_list':searched_project,'message': message,'categorys':categorys,'current_order_products': current_order_products,}

        return render(request, "searching.html",context)
    else:
      message = "You haven't searched for any term"
      return render(request, 'search.html',{"message":message})

@login_required(login_url='login')
def updateItem(request):
    data = json.loads(request.body)
    objectId = data['objectId']
    action = data['action']

    print('Action:', action)
    print('objectId:', objectId)

    profile = request.user.profile
    product = Product.objects.get(id=objectId)
    order, created = Order.objects.get_or_create(profile=profile, complete=False)  

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product) 

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def details(request):
    items_list = Product.objects.all()
    context = {
        'items_list':items_list
    }
    return render(request, 'item_details.html', context)

# def add_to_cart(request, **kwargs):
#     # get the user profile
#     user_profile = get_object_or_404(Profile, user=request.user)
#     # filter products by id
#     product = Product.objects.filter(id=kwargs.get('item_id', "")).first()
#     # check if the user already owns this product
#     # if product in request.user.profile.ebooks.all():
#     #     messages.info(request, 'You already own this ebook')
#     #     return redirect(reverse('product_list')) 
#     # create orderItem of the selected product
#     order_item, status = OrderItem.objects.get_or_create(product=product)
#     # create order associated with the user
#     user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)
#     user_order.items.add(order_item)
#     if status:
#         # generate a reference code
#         user_order.ref_code = generate_order_id()
#         user_order.save()

#     # show confirmation message and redirect back to the same page
#     messages.info(request, "item added to cart")
#     return redirect(reverse('home'))