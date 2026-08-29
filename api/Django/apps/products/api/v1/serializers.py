from apps.products.models import Products, Category
from rest_framework import serializers

from apps.products.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Products
        fields = '__all__'



class ProductWithCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    class Meta:
        model = Products

        fields = [
            'id',
            'title',
            "price",
            'category',
            "description",
        ]
