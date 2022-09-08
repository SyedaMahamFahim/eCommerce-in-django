
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from product.models import *
from myshop.forms import SearchForm
from orders.models import *
from django.contrib.auth.models import User
from user.models import *


def index(request):
    return HttpResponse("Order Page")


@login_required(login_url='/login')  # Check login
def addtoshopcart(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Access User Session information
    checkproduct = ShopCart.objects.filter(
        product_id=id, user_id=current_user.id)
    product = Product.objects.get(pk=id)

    if checkproduct:
        control = 1  # The product is in the cart
    else:
        control = 0

    if request.method == 'POST':  # if there is a post
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1:  # Update  shopcart
                data = ShopCart.objects.get(product_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save()  # save data
            else:  # Inser to Shopcart
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, "Product added to Shopcart ")
        return HttpResponseRedirect(url)
    else:
        if control == 1:
            data = ShopCart.objects.get(product_id=id)
            data.quantity += 1
            data.save()
        else:
            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()
        messages.success(request, "Product added to Shopcart ")
        return HttpResponseRedirect(url)


def shopcart(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity

    total_product = 0
    for rs in shopcart:
        total_product += rs.quantity
    # return HttpResponse(str(total))
    context = {'shopcart': shopcart,
               'category': category,
               'total': total,
               'total_product': total_product, }
    return render(request, 'shopcart.html', context)


@login_required(login_url='/login')  # Check login
def addtowishlist(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Access User Session information
    checkproduct = WishList.objects.filter(
        product_id=id, user_id=current_user.id)
    product = Product.objects.get(pk=id)

    if checkproduct:
        control = 1  # The product is in the cart
    else:
        control = 0

    if request.method == 'POST':  # if there is a post
        form = WishListForm(request.POST)
        if form.is_valid():
            if control == 1:  # Update  shopcart
                data = WishList.objects.get(product_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save()  # save data
            else:  # Inser to Shopcart
                data = WishList()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, "Product added to WishList ")
        return HttpResponseRedirect(url)
    else:
        if control == 1:
            data = WishList.objects.get(product_id=id)
            data.quantity += 1
            data.save()
        else:
            data = WishList()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()
        messages.success(request, "Product added to WishList ")
        return HttpResponseRedirect(url)

def wishlist(request):
    category = Category.objects.all()
    current_user = request.user
    wishlist = WishList.objects.filter(user_id=current_user.id)
    total = 0
    for rs in wishlist:
        total += rs.product.price * rs.quantity

    total_product = 0
    for rs in wishlist:
        total_product += rs.quantity
    # return HttpResponse(str(total))
    context = {'wishlist': wishlist,
               'category': category,
               'total': total,
               'total_product': total_product, }
    return render(request, 'wishlist.html', context)


def checkout(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity
    total_product = 0
    for rs in shopcart:
        total_product += rs.quantity

    if request.method == 'POST':  # if there is a post
        form = OrderForm(request.POST)
        # return HttpResponse(request.POST.items())
        if form.is_valid():
            # Send Credit card to bank,  If the bank responds ok, continue, if not, show the error
            # ..............
            data = Order()
            # get product quantity from form
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.email = form.cleaned_data['email']
            data.phone = form.cleaned_data['phone']
            data.country = form.cleaned_data['country']
            data.city = form.cleaned_data['city']
            data.address_one = form.cleaned_data['address_one']
            data.address_two = form.cleaned_data['address_two']
            data.postal_code = form.cleaned_data['postal_code']
            data.company = form.cleaned_data['company']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(10).upper()  # random cod
            data.code = ordercode
            data.save()

            for rs in shopcart:
                detail = OrderProduct()
                detail.order_id = data.id  # Order Id
                detail.product_id = rs.product_id
                detail.user_id = current_user.id
                detail.quantity = rs.quantity
                detail.price = rs.product.price
                detail.amount = rs.amount
                detail.save() 
                product = Product.objects.get(id=rs.product_id)
                product.quantity -= rs.quantity
                product.save()

            # Clear & Delete shopcart
            ShopCart.objects.filter(user_id=current_user.id).delete()
            request.session['cart_items'] = 0
            messages.success(
                request, "Your Order has been completed. Thank you ")
            return render(request, 'received.html', {'ordercode': ordercode, 'category': category})
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/checkout")

    form = OrderForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    # return HttpResponse(str(total))
    context = {'shopcart': shopcart,
               'category': category,
               'total': total,
               'total_product': total_product,
                'form': form,
               'profile': profile,}

    return render(request, 'checkout.html', context)


@login_required(login_url='/login')  # Check login
def deletefromcart(request, id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Your item has been deleted form Shopcart.")
    return HttpResponseRedirect("/shopcart")

@login_required(login_url='/login')  # Check login
def deletefromwishlist(request, id):
    url = request.META.get('HTTP_REFERER')
    WishList.objects.filter(id=id).delete()
    messages.success(request, "Your item has been deleted form Wishlist.")
    return HttpResponseRedirect(url)    

