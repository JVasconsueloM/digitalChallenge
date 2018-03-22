# Generated by Django 2.0.3 on 2018-03-21 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comun', '0003_auto_20180320_1549'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('id',)},
        ),
        migrations.AlterModelOptions(
            name='productdetails',
            options={'ordering': ('id',)},
        ),
        migrations.AlterField(
            model_name='product',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='modified',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='productdetails',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='productdetails',
            name='modified',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='productdetails',
            name='offer_day_from',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='productdetails',
            name='offer_day_to',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]