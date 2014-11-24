from django.contrib import admin
from privateoffice.models import *
# Register your models here.

class PeopleInline(admin.StackedInline):
    model = People
    extra = 1

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
class ResortAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'resort', 'stars', 'price')

class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'tel')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'hotel', 'status', 'depart')
    inlines = (PeopleInline,)
    search_fields = ['client',]
    list_filter = ('status', 'depart')
    list_editable = ('status',)

admin.site.register(Country, CountryAdmin)
admin.site.register(Resort, ResortAdmin)
admin.site.register(Hotel, HotelAdmin)

admin.site.register(Client, ClientAdmin)
admin.site.register(Order, OrderAdmin)

