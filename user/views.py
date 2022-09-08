

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils import translation

# Create your views here.
from product.models import *
from user.models import UserProfile
from user.forms import SignUpForm
from django.contrib import messages
from orders.models import *
from user.forms import SignUpForm, UserUpdateForm, ProfileUpdateForm

@login_required(login_url='/login') # Check login
def index(request):
    return render(request,'user_profile.html',context)



"""All user detail """
@login_required(login_url='/login') # Check login
def user_profile(request):

    #Account Detail Show 
    category = Category.objects.all()
    current_user = request.user  
    total=0
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    for rs in shopcart:
        total += rs.product.price * rs.quantity

    total_product =0
    for rs in shopcart:
        total_product += rs.quantity  
    profile = UserProfile.objects.get(user_id=current_user.id)  

    #Update 
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user) # request.user is user  data
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return HttpResponseRedirect('/user_profile/')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile) 

    #Update Password 
    if request.method == 'POST':
        update_password_form = PasswordChangeForm(request.user, request.POST)
        if update_password_form.is_valid():
            user = update_password_form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/user_profile')
        else:
            messages.error(request, 'Please correct the error below.<br>'+ str(update_password_form.errors))
            return HttpResponseRedirect('/user_profile')
    else:
        update_password_form = PasswordChangeForm(request.user)
     
    #Show all product information Order
    orders=Order.objects.filter(user_id=current_user.id)
    
    #show all ordered product
    order_product = OrderProduct.objects.filter(user_id=current_user.id).order_by('-id')

    #Show All Comments 
    comments = Comment.objects.filter(user_id=current_user.id)

    #Show All Wishlist 
    wishlist=WishList.objects.filter(user_id=current_user.id)
    context = {'shopcart': shopcart,
               'category': category,
               'total': total,
               'total_product': total_product,
               'profile': profile,
               'user_form': user_form,
               'profile_form': profile_form,
               'update_password_form':update_password_form,
               'orders':orders,
               'order_product':order_product,
               'comments':comments,
               'wishlist':wishlist}

    return render(request,'user_profile.html',context)



@login_required(login_url='/login') # Check login
def user_orderdetail(request,id):
    category = Category.objects.all()
    current_user = request.user  
    total=0
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    for rs in shopcart:
        total += rs.product.price * rs.quantity

    total_product =0
    for rs in shopcart:
        total_product += rs.quantity  
    profile = UserProfile.objects.get(user_id=current_user.id)  
    order = Order.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderProduct.objects.filter(order_id=id)
    context = {
        'shopcart': shopcart,
        'category': category,
        'total': total,
        'total_product': total_product,
        'order': order,
        'orderitems': orderitems,
        'profile':profile,
    }
    return render(request, 'orderdetail.html', context) 

@login_required(login_url='/login') # Check login
def user_order_product_detail(request,id,oid):
    category = Category.objects.all()
    current_user = request.user  
    total=0
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    for rs in shopcart:
        total += rs.product.price * rs.quantity

    total_product =0
    for rs in shopcart:
        total_product += rs.quantity  
    profile = UserProfile.objects.get(user_id=current_user.id)  
    order = Order.objects.get(user_id=current_user.id, id=oid)
    orderitems = OrderProduct.objects.filter(id=id,user_id=current_user.id)
    context = {
        'shopcart': shopcart,
        'category': category,
        'total': total,
        'total_product': total_product,
        'profile':profile,
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'orderdetail.html', context)

@login_required(login_url='/login') # Check login
def user_order_product_detail(request,id,oid):
    category = Category.objects.all()
    current_user = request.user  
    total=0
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    for rs in shopcart:
        total += rs.product.price * rs.quantity

    total_product =0
    for rs in shopcart:
        total_product += rs.quantity  
    profile = UserProfile.objects.get(user_id=current_user.id)  
    order = Order.objects.get(user_id=current_user.id, id=oid)
    orderitems = OrderProduct.objects.filter(id=id,user_id=current_user.id)
    context = {
        'shopcart': shopcart,
        'category': category,
        'total': total,
        'total_product': total_product,
        'profile':profile,
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'single_order_product_detail.html', context)

@login_required(login_url='/login') # Check login
def user_deletecomment(request,id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Comment deleted..')
    return HttpResponseRedirect('/user_profile')
def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user =request.user
            userprofile=UserProfile.objects.get(user_id=current_user.id)
            request.session['userimage'] = userprofile.image.url
            
            # Redirect to a success page.
            return HttpResponseRedirect('/')
        else:
            messages.warning(
                request, "Login Error !! Username or Password is incorrect")
            return HttpResponseRedirect('/login')
    # Return an 'invalid login' error message.
    category = Category.objects.all()
    product_sliders = Product.objects.all().order_by('-id')[:4]
    context = {
        'category': category,
        'products_slider': product_sliders,
    }
    return render(request, 'login.html', context)

    # Return an 'invalid login' error message.


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save() #completed sign up
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            # Create data in profile table for user
            current_user = request.user
            data=UserProfile()
            data.user_id=current_user.id
            data.image="images/users/user.png"
            data.save()
            messages.success(request, 'Your account has been created!')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request,form.errors)
            return HttpResponseRedirect('/signup')
    form = SignUpForm()        
    category = Category.objects.all()
    product_sliders = Product.objects.all().order_by('-id')[:4]
    context = {
        'category': category,
        'products_slider': product_sliders,
        'form': form,
    }
    return render(request, 'signup.html', context)

def logout_function(request):
    logout(request)
    return HttpResponseRedirect('/')