from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    
    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product', null=True)
    
    title = models.CharField(max_length=250)
    brand = models.CharField(max_length=250, default="un-branded")
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=250)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to="images/")
    
    class Meta:
        verbose_name_plural = "products"

    def __str__(self):
        return self.title