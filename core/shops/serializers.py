from rest_framework import serializers
from .models import Product, ProductCategory, ProductImage


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['name',  'description', 'slug']


class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer()
    in_stock = serializers.BooleanField(source='is_in_stock', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'name', 'slug',
            'description', 'price_in_sats', 'stock_quantity',
            'is_active', 'in_stock', 'images',
            'created_at', 'updated_at'
        ]


class ProductImageSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'order','product']