from django.db import models
from django.forms.models import model_to_dict
from django.utils import timezone

from apps.comun.constants import TYPE_PRODUCTS, FAMILIES, PRODUCT, HOME


class Brand(models.Model):
    name = models.TextField(max_length=150)
    # ... other fields


class Product(models.Model):
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    type = models.CharField(max_length=2, choices=TYPE_PRODUCTS, default=PRODUCT)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    is_variation = models.BooleanField(default=False)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, blank=True, null=True)
    code = models.IntegerField(blank=True, null=True)
    family = models.CharField(max_length=2, choices=FAMILIES, default=HOME)
    is_complement = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)

    class Meta:
        ordering = ('id',)

    @staticmethod
    def fields():
        return list(field.name for field in Product._meta.fields)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            if not self.created:
                self.created = timezone.now()
        else:
            self.modified = timezone.now()
        return super(Product, self).save(*args, **kwargs)

    def to_dict(self, add_childs=True):
        model_dict = model_to_dict(self)
        if add_childs:
            model_dict['details'] = self.details.all().values()
        return model_dict


class ProductDetails(models.Model):
    product = models.ForeignKey(Product, related_name='details', on_delete=models.CASCADE)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_visibility = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    price_offer = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    offer_day_from = models.DateTimeField(blank=True, null=True)
    offer_day_to = models.DateTimeField(blank=True, null=True)
    quantity = models.IntegerField(default=0)
    sku = models.IntegerField(default=0)

    class Meta:
        ordering = ('id',)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            if not self.created:
                self.created = timezone.now()
        else:
            self.modified = timezone.now()
        return super(ProductDetails, self).save(*args, **kwargs)
