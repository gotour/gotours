from django.contrib import admin
from .models import Tourist,Contact,Destinations,Book_trip,Transaction
# Register your models here.
admin.site.register(Tourist)
admin.site.register(Contact)
admin.site.register(Destinations)
admin.site.register(Book_trip)
admin.site.register(Transaction)