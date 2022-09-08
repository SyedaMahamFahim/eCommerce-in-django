

from django.urls import path
from . import views
from shopping import settings

urlpatterns = [
    path("", views.index, name="index"),
    path("homebase", views.homebase, name="homebase"),
    path("contact", views.contact, name="contact"),
    path("aboutus", views.aboutus, name="aboutus"),
    path("faqs", views.faqs, name="faqs"),
    path("demo", views.demo, name="demo"),
    path("demo_two", views.demo_two, name="demo_two"),
    path("category_products", views.category_products, name="category_products"),
    path("product_detail", views.product_detail, name="product_detail"),
    path("productdetail", views.productdetail, name="productdetail"), 
    path("shop", views.shop, name="shop"), 
    path("search", views.search, name="search"), 
    path("shipping_detail", views.shipping_detail, name="shipping_detail"),  
]

