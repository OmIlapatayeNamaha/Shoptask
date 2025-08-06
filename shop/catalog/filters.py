import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    min_price=django_filters.NumberFilter(field_name="price",lookup_expr="gte")
    max_price=django_filters.NumberFilter(field_name="price",lookup_expr="gte")
    status=django_filters.CharFilter(field_name="status")
    category=django_filters.NumberFilter(field_name="category_id")
    class Meta:
        model=Product
        fields=['status','category','min_price','max_price']