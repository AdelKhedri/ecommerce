from django.urls import path
from django.views.generic import TemplateView


app_name = "shop"
urlpatterns = [
    path('product/details/<int:pk>/', TemplateView.as_view(), name="product-detail")
]