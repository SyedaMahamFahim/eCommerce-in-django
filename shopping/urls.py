"""shopping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from myshop import views
from orders import views as OrderViews
from user import views as UserViews
from django.views.static import serve
from django.conf.urls import url


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include('myshop.urls')),
    path('product/', include('product.urls')),
    path('orders/', include('orders.urls')),
    path('user/', include('user.urls')),

    path('shopcart/', OrderViews.shopcart, name='shopcart'),
    path('wishlist/', OrderViews.wishlist, name='wishlist'),
    path('checkout/', OrderViews.checkout, name='checkout'),
    path('login/', UserViews.login_form, name='login'),
    path('user_profile/', UserViews.user_profile, name='user_profile'),
    path('orderdetail/<int:id>', UserViews.user_orderdetail, name='user_orderdetail'),
    path('single_order_product_detail/<int:id>/<int:oid>', UserViews.user_order_product_detail, name='user_order_product_detail'),
    path('deletecomment/<int:id>', UserViews.user_deletecomment, name='user_deletecomment'),
    path('logout/', UserViews.logout_function, name='logout_function'),
    path('signup/', UserViews.signup, name='signup'),

    path('search/', views.search, name='search'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('category/<int:id>/<slug:slug>',views.category_products,name='category_products'), 
    
    path('product/<int:id>/<slug:slug>',views.product_detail,name='product_detail'),
    path('category/product/<int:id>/<slug:slug>',views.productdetail,name='productdetail'),
    path('ajaxcolor/', views.ajaxcolor, name='ajaxcolor'),
    # url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    # url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = 'myshop.views.error_404_view'
