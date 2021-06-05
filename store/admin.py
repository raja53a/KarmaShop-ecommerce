from django.contrib import admin
from .models import HomeContent, Product, Brand, ReviewRating, Variation, ProductGallery, BrandLogo
import admin_thumbnails
from django.utils.html import format_html

# Register your models here.

@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" >'.format(object.images.url))
    thumbnail.short_description = 'Profile Picture'
    prepopulated_fields = {'slug':('product_name',)}
    list_display = ('display_image','brand','product_name','price','slug','is_available')
    #list_display = ('display_image','category_name','slug')
    list_display_links = ('display_image','product_name')
    inlines = [ProductGalleryInline]
    
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','variation_category','variation_value','is_active','created_date')
    list_display_links = ('product','variation_category','variation_value')
    list_editable = ('is_active',)
    list_filter = ('product','variation_category','variation_value')

admin.site.register(Product,ProductAdmin)
admin.site.register(Brand)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)
admin.site.register(HomeContent)
admin.site.register(BrandLogo)