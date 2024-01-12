"""
Defines the admin interface for the models in the app
"""
from django.contrib import admin
from .models import CarMake, CarModel

# Register models
admin.site.register(CarMake)
admin.site.register(CarModel)

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'make', 'year')
    list_filter = ('make', 'year')
    search_fields = ('name', 'make__name', 'year')
    inlines = [CarModelInline]

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
