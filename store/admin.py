from django.contrib import admin
from .models import Product, Brand, Variation
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('product_name',)}
    list_display = ('display_image','brand','product_name','price','slug','is_available')
    #list_display = ('display_image','category_name','slug')
    list_display_links = ('display_image','product_name')
    
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','variation_category','variation_value','is_active','created_date')
    list_display_links = ('product','variation_category','variation_value')
    list_editable = ('is_active',)
    list_filter = ('product','variation_category','variation_value')
admin.site.register(Product,ProductAdmin)
admin.site.register(Brand)
admin.site.register(Variation, VariationAdmin)