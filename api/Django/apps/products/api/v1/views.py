from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializers import ProductWithCategorySerializer, ProductSerializer
from ...models import Product




class ProductListAPIView(ListAPIView):
    def get_queryset(self):
        if self.request.query_params.get('optimize', '').lower() == 'true':
            return Product.objects.all().prefetch_related('categories')
        return Product.objects.all()

    def get_serializer_class(self):
        if self.request.query_params.get('with_category', '').lower() == 'true':
            return ProductWithCategorySerializer
        return ProductSerializer


class ProductDetailAPIView(RetrieveAPIView):
    lookup_field = 'id'

    def get_queryset(self):
        if self.request.query_params.get('optimize', '').lower() == 'true':
            return Product.objects.all().prefetch_related('categories')
        return Product.objects.all()

    def get_serializer_class(self):
        if self.request.query_params.get('with_category', '').lower() == 'true':
            return ProductWithCategorySerializer
        return ProductSerializer