from django.contrib import admin
from .models import Product,Variation, ReviewRating

# Register your models here.
class productAdmin(admin.ModelAdmin):
    list_display = ('product_name' ,'price', 'stock', 'category' ,'modified_date','is_avilable','is_featured','today_offer','shoes_pair')
    prepopulated_fields = {'slug' :('product_name',)}
    list_editable = ('is_featured','today_offer','shoes_pair')

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','variation_category','variation_value','is_active')
    list_editable = ('is_active',)
    list_filter  = ('product', 'variation_category','variation_value','is_active')

admin.site.register(Product,productAdmin)
admin.site.register(Variation ,VariationAdmin)
admin.site.register(ReviewRating)