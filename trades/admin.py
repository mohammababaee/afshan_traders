from django.contrib import admin
from .models import Portfolio, Trade, Stock
# Register your models here.
admin.site.register(Portfolio)
admin.site.register(Trade)
admin.site.register(Stock)

