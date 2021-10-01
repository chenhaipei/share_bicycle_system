from django.contrib import admin
from .models import Bike, Customer, Transaction, Record


admin.site.site_header = 'Bikes System Dashboard'
admin.site.site_title = 'Bikes System Dashboard'


class BikesAdmin(admin.ModelAdmin):
    list_display = ('unique', 'position', 'available')
    list_filter = ['available']
    search_fields = ['position']


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('unique', 'account', 'balance')
    search_fields = ['unique']


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('unique', 'customer', 'bike', 'start_time', 'status')
    list_filter = ['customer', 'bike', 'status']
    search_fields = ['unique']


class RecordAdmin(admin.ModelAdmin):
    list_display = ('unique', 'customer', 'bike', 'status', 'created')
    list_filter = ['customer', 'bike', 'status']
    search_fields = ['customer']


admin.site.register(Bike, BikesAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Record, RecordAdmin)
