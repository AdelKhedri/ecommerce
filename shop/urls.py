from django.urls import path, re_path
from . import views


app_name = "shop"
urlpatterns = [
    path('product/details/<int:pk>/', views.ProductDetailView.as_view(), name="product-detail"),
    re_path('^update-cart', views.UpdateCartView.as_view(), name="update cart"),
    # path('categorys', views.CategoryView.as_view(), name="categorys"),
    re_path(r'^category/(?P<slug>[-\w]+)/$', views.CategoryView.as_view(), name="category view"),
    re_path('^categorys/', views.CategorysListView.as_view(), name="categorys list"),
    path('cart/', views.CartUnRegisteredUserView.as_view(), name="cart for unregistered user"),
]