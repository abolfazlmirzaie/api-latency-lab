from django.urls import path

from apps.products.api.v1.views import ProductDetailAPIView, ProductListAPIView

urlpatterns = [
    path('products/<int:id>/', ProductDetailAPIView.as_view()),
    path('products/', ProductListAPIView.as_view()),
]