from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("user_profile/", views.user_profile, name="user_profile"),
    path('orderdetail/<int:id>', views.user_orderdetail, name='user_orderdetail'),
    path('single_order_product_detail/<int:id>/<int:oid>', views.user_order_product_detail, name='user_order_product_detail'),
]

