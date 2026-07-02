from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, default='bi-grid')

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.CharField(max_length=255, default='placeholder.jpg')
    rating = models.FloatField(default=5.0)
    sold_count = models.IntegerField(default=0)
    location = models.CharField(max_length=100, default='กรุงเทพมหานคร')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    stock = models.IntegerField(default=10)

    def __str__(self):
        return self.name
