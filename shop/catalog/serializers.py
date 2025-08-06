from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','name']

class ProductSerializer(serializers.ModelSerializer):
    _category=serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    class Meta:
        model= Product
        fields=['id','Category','title','description','price','status','created_at','updated_at']
        read_only_fields=['created_at','updated_at']