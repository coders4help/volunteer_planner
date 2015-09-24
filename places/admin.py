from django.contrib import admin

from .models import Country, Region, Area, Municipality

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = (u'id', 'name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ['name']}

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = (u'id', 'name', 'country', 'slug')
    list_filter = ('country',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ['name']}

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = (u'id', 'region', 'name', 'slug')
    list_filter = ('region',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ['name']}

@admin.register(Municipality)
class MunicipalityAdmin(admin.ModelAdmin):
    list_display = (u'id', 'area', 'name', 'slug')
    list_filter = ('area',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ['name']}
