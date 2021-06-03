from django.contrib import admin
from .models import Category
from django.contrib.admin.models import LogEntry
# Register your models here.
LogEntry.objects.all().delete()

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}
    list_display = ('category_name','slug')
    #list_display = ('display_image','category_name','slug')
    #list_display_links = ('display_image','category_name')
    
admin.site.register(Category,CategoryAdmin)