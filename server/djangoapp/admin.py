"""
Defines the admin interface for the models in the app
"""
from django.contrib import admin
from .models import CarMake, CarModel

# Register models
admin.site.register(CarMake)
admin.site.register(CarModel)

class CarModelInline(admin.StackedInline):
    """
    Represents an inline model admin for CarModel.
    """
    model = CarModel

class CarModelAdmin(admin.ModelAdmin):
    """
    Admin class for managing CarModel objects in the Django admin interface.
    """
    list_display = ('name', 'make', 'year')
    list_filter = ('make', 'year')
    search_fields = ('name', 'make__name', 'year')
    inlines = [CarModelInline]

class CarMakeAdmin(admin.ModelAdmin):
    """
    Admin class for managing CarMake objects.
    
    This class defines the behavior of the admin interface for CarMake objects.
    It includes the `CarModelInline` inline model for managing related CarModel objects.
    """
    inlines = [CarModelInline]
