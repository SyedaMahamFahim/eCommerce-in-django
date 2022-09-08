from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from .models import Contact
from django.conf import settings
from product.models import *
from myshop.forms import SearchForm
from orders.models import *
from orders.views import *
from django.contrib.auth.models import User
from user.models import *
from datetime import datetime
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def error_404_view(request, exception):
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity

    total_product = 0
    for rs in shopcart:
        total_product += rs.quantity
    context = {
        'category': category,
        'shopcart': shopcart,
        'category': category,
        'total': total,
        'total_product': total_product,
    }
    return render(request,'404.html',context)

@login_required(login_url='/login')  # Check login
def deletefromcart(request, id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Your item has been deleted form Shopcart.")
    return HttpResponseRedirect("/shopcart")


def index(request):

    category = Category.objects.all()
    product_sliders = Product.objects.all().order_by(
        '-id')[:4]  # Product Slider
    lastest_product = Product.objects.all().order_by(
        '-id')[:3]  # Lastest Prodcut
    recommanded_product = Product.objects.all().order_by('?')[
        :3]  # Random Product
    viewed_product = Product.objects.all().order_by('id')[:3]
    hometab_lastest_product = Product.objects.all().order_by('-id')[:8]
    hometab_recommanded_product = Product.objects.all().order_by('?')[:8]
    hometab_men_product = Product.objects.filter(category=5)  # Men Category
    hometab_women_product = Product.objects.filter(category=8)  # Women Category
    top_view_product = Product.objects.all().order_by('-num_of_visits')[:8]
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity

    total_product = 0
    for rs in shopcart:
        total_product += rs.quantity
    context = {
        'category': category,
        'products_slider': product_sliders,
        'lastest_product': lastest_product,
        'recommanded_product': recommanded_product,
        'viewed_product': viewed_product,
        'hometab_lastest_product': hometab_lastest_product,
        'hometab_recommanded_product':   hometab_recommanded_product,
        'shopcart': shopcart,
        'total': total,
        'total_product': total_product,
        'hometab_men_product': hometab_men_product,
        'hometab_women_product': hometab_women_product,
        'top_view_product': top_view_product,
    }
    return render(request,'index.html', context)


def homebase(request):
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity

    total_product = 0
    for rs in shopcart:
        total_product += rs.quantity
    # return HttpResponse(str(total))
    context = {'category': category,
               'shopcart': shopcart,
               'category': category,
               'total': total,
               'total_product': total_product,
               }
    return render(request, 'homebase.html', context)


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')

        if len(name) < 2 or len(email) < 3 or len(phone) < 10 or len(desc) < 4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact = Contact(name=name, email=email, phone=phone, desc=desc)
            contact.save()
            messages.success(
                request, "Your message has been successfully sent")

    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity

    total_product = 0
    for rs in shopcart:
        total_product += rs.quantity
    context = {
        'category': category,
        'shopcart': shopcart,
        'category': category,
        'total': total,
        'total_product': total_product,
    }
    return render(request, 'contact.html', context)


def aboutus(request):
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity

    total_product = 0
    for rs in shopcart:
        total_product += rs.quantity
    context = {
        'category': category,
        'shopcart': shopcart,
        'category': category,
        'total': total,
        'total_product': total_product,
    }
    return render(request, 'aboutus.html', context)


def faqs(request):
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity

    total_product = 0
    for rs in shopcart:
        total_product += rs.quantity
    context = {
        'category': category,
        'shopcart': shopcart,
        'category': category,
        'total': total,
        'total_product': total_product,
    }
    return render(request, 'faqs.html', context)


def shipping_detail(request):
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity

    total_product = 0
    for rs in shopcart:
        total_product += rs.quantity
    context = {
        'category': category,
        'shopcart': shopcart,
        'category': category,
        'total': total,
        'total_product': total_product,
    }
    return render(request, 'shipping_detail.html', context)

#""
def demo(request):
    category = Category.objects.all()
    product_sliders = Product.objects.all().order_by('-id')[:4]
    lastest_product = Product.objects.all().order_by('-id')[:3]
    recommanded_product = Product.objects.all().order_by('?')[:3]
    viewed_product = Product.objects.all().order_by('id')[:3]
    hometab_lastest_product = Product.objects.all().order_by('-id')[:8]
    hometab_recommanded_product = Product.objects.all().order_by('?')[:8]
    deletecard = shopcart(request)
    context = {
        'category': category,
        'products_slider': product_sliders,
        'lastest_product': lastest_product,
        'recommanded_product': recommanded_product,
        'viewed_product': viewed_product,
        'hometab_lastest_product': hometab_lastest_product,
        'hometab_recommanded_product': hometab_recommanded_product,
        'deletecard': deletecard,
    }
    return render(request, 'demo.html', context)


def shop(request):
    category = Category.objects.all()
    # all_products=Product.objects.all()
    products = Product.objects.all()
    paginator = Paginator(products, 3)
    page = request.GET.get('page')
   
    products = paginator.get_page(page)

    recently_view_product = Product.objects.all().order_by('-last_visit')[:4]
    # Cart View
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity

    total_product = 0
    for rs in shopcart:
        total_product += rs.quantity

    context = {
        'products': products,
        # 'all_products':all_products,
        'category': category,
        'shopcart': shopcart,
        'total': total,
        'total_product': total_product,
        'recently_view_product': recently_view_product,
    }
    return render(request, 'shop.html', context)


def product_detail(request, id, slug):

    product = Product.objects.get(pk=id)
    product = get_object_or_404(Product, id=id)
    category = Category.objects.all()
    # if pk==id is
    # products=Product.objects.filter(category_id=id)

    product.num_of_visits = product.num_of_visits+1
    product.last_visit = datetime.now()
    product.save()
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id,status='True')
    paginator = Paginator(comments, 3)
    page = request.GET.get('page')
   
    comments = paginator.get_page(page)

    # Product Slider
    product_sliders = Product.objects.filter().order_by('-id')[:4]

    # Cart View
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity

    total_product = 0
    for rs in shopcart:
        total_product += rs.quantity

    context = {
        'product': product,
        'category': category,
        'images': images,
        'comments': comments,
        'products_slider': product_sliders,
        'shopcart': shopcart,
        'total': total,
        'total_product': total_product,
        #
    }
    return render(request, 'product_detail.html', context)


def productdetail(request, id, slug):
    # Product Comment
    query = request.GET.get('q')
    product = Product.objects.get(pk=id)
    category = Category.objects.all()
    # if pk==id is
    products = Product.objects.filter(category_id=id)
    # cat_main=Category.objects.filter(category_id=id)

    product.num_of_visits=product.num_of_visits+1
    product.save()
    product.last_visit=datetime.now()

    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id, status='True')

    # Product Slider
    product_sliders = Product.objects.filter().order_by('-id')[:4]

    # Cart View
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity

    total_product = 0
    for rs in shopcart:
        total_product += rs.quantity

    context = {
        'product': product,
        'category': category,
        'images': images,
        'comments ': comments,
        'products_slider': product_sliders,
        'shopcart': shopcart,
        'total': total,
        'total_product': total_product,
    }

    if product.variant != "None":  # Product have variants
        if request.method == 'POST':  # if we select color
            variant_id = request.POST.get('variantid')
            # selected product by click color radio
            variant = Variants.objects.get(
                id=variant_id, product_id=id, size_id=variant.size_id)
            sizes = Variants.objects.raw(
                'SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id', [id])
            query += variant.title+' Size:' + \
                str(variant.size) + ' Color:' + str(variant.color)
        else:
            variants = Variants.objects.filter(product_id=id)
            colors = Variants.objects.filter(
                product_id=id, size_id=variants[0].size_id)
            sizes = Variants.objects.raw(
                'SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id', [id])
            variant = Variants.objects.get(id=variants[0].id)

        context.update({'sizes': sizes, 'colors': colors,
                        'variant': variant, 'query': query
                        })
    return render(request, 'productdetail.html', context)


def ajaxcolor(request):
    data = {}
    if request.POST.get('action') == 'post':
        size_id = request.POST.get('size')
        productid = request.POST.get('productid')
        colors = Variants.objects.filter(product_id=productid, size_id=size_id)
        context = {
            'size_id': size_id,
            'productid': productid,
            'colors': colors,
        }
        data = {'rendered_table': render_to_string(
            'color_list.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)


"""
 # 'products':products,
        
        # 'related_products':related_products,
def category_products(request,id,slug):
    category=Category.objects.all()
    products=Product.objects.filter(category_id=id) 
    context={
        'category':category,
        'products':products,
    }
    return render(request,'product_detail.html',context)
"""


def demo_two(request):
    category = Category.objects.all()
    products = Product.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(products, 10)
    try:
        product = paginator.page(page)
    except PageNotAnInteger:
        product = paginator.page(1)
    except EmptyPage:
        product = paginator.page(paginator.num_pages)

    comments = Comment.objects.filter(status='True')
    product_sliders = Product.objects.filter().order_by('-id')[:4]
    lastest_product = Product.objects.filter().order_by('-id')[:3]
    recommed_product = Product.objects.filter().order_by('?')[:3]
    allproduct = Product.objects.filter(category=9)  # Men shoes

    context = {
        'category': category,
        'products_slider': product_sliders,
        'lastest_product': lastest_product,
        'recommed_product': recommed_product,
        'allproduct': allproduct,
        'comments': comments,
        'products': products,
        'product': product,
    }
    return render(request, 'demo_two.html', context)


def category_products(request, id, slug):
    category = Category.objects.all()
    products = Product.objects.filter(category_id=id)
    paginator = Paginator(products, 3)
    page = request.GET.get('page')
   
    products = paginator.get_page(page)

    recently_view_product = Product.objects.all().order_by('-last_visit')[:4]
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity

    total_product = 0
    for rs in shopcart:
        total_product += rs.quantity
    context = {
        'category': category,
        'products': products,
        'shopcart': shopcart,
        'category': category,
        'total': total,
        'total_product': total_product,
        'recently_view_product':recently_view_product,
    }
    return render(request, 'category_products.html', context)


"""
def search2(request):
	q=request.GET['q']
	data=Product.objects.filter(title__icontains=q).order_by('-id')
	return render(request,'search.html',{'data':data})
"""


def search(request):
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity

    total_product = 0
    for rs in shopcart:
        total_product += rs.quantity

    if request.method == 'GET':
        query = request.GET.get('q')

        submitbutton = request.GET.get('submit')

        if query is not None:
            results = Product.objects.filter(
                title__icontains=query).order_by('-id')

            context = {'results': results,
                       'submitbutton': submitbutton,
                       'shopcart': shopcart,
                       'category': category,
                       'total': total,
                       'total_product': total_product, }

            return render(request, 'search.html', context)

        else:
            return render(request, 'search.html')

    else:
        return render(request, 'search.html')


