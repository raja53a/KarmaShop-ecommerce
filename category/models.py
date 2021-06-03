from django.db import models
from django.urls import reverse
# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50,unique=True)
    slug  = models.SlugField(max_length=100, unique= True)
    description = models.TextField(max_length=255, blank=True)
    category_img = models.ImageField(upload_to='category/', blank=True, null=True)

    #def display_image(self):
        #return mark_safe('<img src="{}" width="100" />'.format(self.category_img.url))
    #display_image.short_description = 'Image'
    #display_image.allow_tags = True
    def get_url(self):
            return reverse('products_by_category',args=[self.slug])
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name