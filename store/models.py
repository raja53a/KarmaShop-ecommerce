from django.db import models
from django.db.models.deletion import CASCADE
from django.urls import reverse
from django.utils import timezone
from category.models import Category
from django.utils.safestring import mark_safe
# Create your models here.
class Product(models.Model):
    product_name        = models.CharField(max_length=200,unique=True)
    brand               = models.ForeignKey('Brand', on_delete=models.SET_NULL, null=True)
    product_category    = models.ForeignKey(Category, on_delete = models.SET_NULL, null = True)
    slug                = models.SlugField(max_length=255, unique= True)
    price               = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    description         = models.TextField(max_length=255, blank=True)
    product_img         = models.ImageField(upload_to='product/', blank=True, null=True)
    created             = models.DateTimeField(auto_now_add=True)
    modified_time       = models.DateTimeField(auto_now=True)
    stock               = models.IntegerField(null=True)
    is_available        = models.BooleanField(default=True)

    def get_url(self):
        return reverse('products_detail',args=[self.product_category.slug,self.slug])

    def display_image(self):
        return mark_safe('<img src="{}" width="100" />'.format(self.product_img.url))
    display_image.short_description = 'Image'
    display_image.allow_tags = True

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.product_name

class Brand(models.Model):
    brand_name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'brand'
        verbose_name_plural = 'brands'
        
    def __str__(self):
        return self.brand_name


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)

variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value     = models.CharField(max_length=100)
    is_active           = models.BooleanField(default=True)
    created_date        = models.DateTimeField(auto_now=True)

    objects = VariationManager()
    
    def __str__(self):
        return self.variation_value
