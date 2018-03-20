from django.db import models

from apps.comun.constants import TYPE_PRODUCTS, FAMILIES, PRODUCT, HOME


class Brand(models.Model):
    name = models.TextField(max_length=150)
    # ... other fields


class Product(models.Model):
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    type = models.CharField(max_length=2, choices=TYPE_PRODUCTS, default=PRODUCT)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    is_variation = models.BooleanField()
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, blank=True, null=True)
    code = models.IntegerField(blank=True, null=True)
    family = models.CharField(max_length=2, choices=FAMILIES, default=HOME)
    is_complement = models.BooleanField()
    is_delete = models.BooleanField()

    @staticmethod
    def fields():
        return list(field.name for field in Product._meta.fields)


class ProductDetails(models.Model):
    product = models.ForeignKey(Product, related_name='details', on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_visibility = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    price_offer = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    offer_day_from = models.DateField(blank=True, null=True)
    offer_day_to = models.DateField(blank=True, null=True)
