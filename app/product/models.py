from django.db import models
from django.utils.html import format_html
from django.contrib import admin



class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    product_storage_address = models.CharField(max_length=255)
    price_brl = models.FloatField()

    def __str__(self):
        return self.name


class PaymentType(models.Model):
    payment_type = models.CharField(
        max_length=255,
        choices=[
            ("credit_card", "Credit Card"),
            ("debit_card", "Debit Card"),
            ("boleto", "Boleto"),
        ],
    )
    description = models.TextField()

    @admin.display
    def colored_payment_type(self):
        color = {
            "credit_card": "blue",
            "debit_card": "green",
            "boleto": "red",
        }
        return format_html(
            f'<span style="color: {color[self.payment_type]}">{self.payment_type.upper()}</span>'
        )

    def __str__(self):
        return self.payment_type    

