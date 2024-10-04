import aiohttp
import asyncio
from django.contrib import admin
from product.models import Product, PaymentType


class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "manufacturer", "price_brl", "price_usd")
    search_fields = ("name", "category", "manufacturer")
    list_filter = ("category", "manufacturer")

    # creating a new field in the admin panel
    async def get_exchange_rate(self):
        url = "https://economia.awesomeapi.com.br/last/BRL-USD"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                exchange_rate = float(data["BRLUSD"]["bid"])
                return float(exchange_rate)

    def price_usd(self, obj):
        try:
            exchange_rate = asyncio.run(self.get_exchange_rate())
        except Exception as e:
            print(f"Error: {e}")
            exchange_rate = 0 # that will indicate error
    
        return round(obj.price_brl*exchange_rate, 2)   
    
    class Meta:
        model = Product


class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ("payment_type", "description", "colored_payment_type")
    search_fields = ("payment_type", "description")

 
    class Meta:
        model = PaymentType


admin.site.register(Product, ProductAdmin)
admin.site.register(PaymentType, PaymentTypeAdmin)
admin.sites.AdminSite.site_header = "Anima Test ADMIN"

