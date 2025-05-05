from rest_framework import serializers
from .models import Product, ProductImage, ProductCategory


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    categories = ProductCategorySerializer(read_only=True)

    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'order', 'categories']

class ProductSerializer(serializers.ModelSerializer):
    products = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price_in_sats', 'images','products']