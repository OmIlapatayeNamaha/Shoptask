from django.db import models

class Category(models.Model):
    name=models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.name

STATUS_CHOICES=(('active','inactive'),('inactive','inactive'))
class Product(models.Model):
    Category=models.ForeignKey(Category, on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    description=models.TextField(blank=True)
    price=models.DecimalField(max_digits=12, decimal_places=2)
    status=models.CharField(max_length=8, choices=STATUS_CHOICES, default='active')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)


