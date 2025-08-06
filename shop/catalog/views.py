from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone
import csv
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .filters import ProductFilter
from django.http import HttpResponse
from .tasks import create_dummy_products

class LoginView(TokenObtainPairView):
    permission_classes=[AllowAny]

class RefreshView(TokenRefreshView):
    permission_classes=[AllowAny]

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=Category.objects.all().order_by("id")
    serializer_class=CategorySerializer
    http_method_names=["get","post","head","options"]

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=Product.objects.select_related("category").all().order_by("-id")
    serializer_class=ProductSerializer
    filterset_class=ProductFilter
    search_fields=["title","description"]
    ordering_fields=["price", "created_at", "updated_at"]

    def perform_create(self, serializer):
        product=serializer.save()
        try:
            n=int(self.request.query_params.get("dummy_count","10"))
        except ValueError:
            n=10
            create_dummy_products.delay(Product.category_id,n)
    @action(detail=False,
    methods=["post"], url_path="generate-dummy")
    def generate_dummy(self, request):
        cat_id=int(request.data.get("category_id"))
        count=int(request.data.get("count",1000))
        task=create_dummy_products.delay(cat_id, count)
        return Response({"task_id":task.id, "queued":True,"count":count},status=202)
    
    @action(detail=False, methods=["get"],url_path="export/csv",permission_classes=[])
    def export_csv(self,request):
        qs=self.filter_queryset(self.get_queryset())
        response=HttpResponse(content_type="text/csv")
        filename=f"products_{timezone.now().strftime('%Y%m%d_%H%M%S')}.csv"
        response["Content-Disposition"]=f'attachment; filename="{filename}"'
        writer=csv.writer(response)
        writer.writerow(["id","category_id","title","description","price","status","created_at","updated_at"])
        for p in qs:
            writer.writerow([p.id,p.category_id,p.title,p.description,p.price,p.status,p.created_at,p.updated_at])
            return response
    def export_xlsx(self,request):
        qs=self.filter_queryset(self.get_queryset())
        wb=Workbook()
        ws=wb.active
        ws.append(["id","category_id","title","description","price","status","created_at","updated_at"])
        for p in qs:
            ws.append([p.id,p.category_id,p.title,p.description,p.status,p.created_at,p.updated_at])

        from io import BytesIO 
        buffer=BytesIO()
        wb.save(buffer)
        buffer.seek(0)
        response=HttpResponse(buffer.read())