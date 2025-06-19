from . import models

from django.contrib import admin

# Register your models here.
@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'image']
    list_display_links = ['pk', 'title']
    prepopulated_fields = {
        'slug': ('title',)
    }


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    extra = 1


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']
    list_display_links = ['pk', 'name']
    search_fields = ['name']
    inlines = [ProductImageInline]

# admin - admin