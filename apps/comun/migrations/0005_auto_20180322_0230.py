# Generated by Django 2.0.3 on 2018-03-22 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comun', '0004_auto_20180321_1853'),
    ]

    operations = [
        migrations.AddField(
            model_name='productdetails',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='productdetails',
            name='sku',
            field=models.IntegerField(default=0),
        ),
    ]