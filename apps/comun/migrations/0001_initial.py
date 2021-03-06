# Generated by Django 2.0.3 on 2018-03-20 19:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(auto_created=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('modified', models.DateField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('type', models.CharField(choices=[('PR', 'Product'), ('SR', 'Other')], default='PR', max_length=2)),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_variation', models.BooleanField()),
                ('family', models.CharField(choices=[('1', 'Home'), ('2', 'Home')], default='1', max_length=2)),
                ('is_complement', models.BooleanField()),
                ('is_delete', models.BooleanField()),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='comun.Brand')),
            ],
        ),
        migrations.CreateModel(
            name='ProductDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True)),
                ('modified', models.DateField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_visibility', models.BooleanField(default=True)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('price_offer', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('offer_day_from', models.DateField(blank=True, null=True)),
                ('offer_day_to', models.DateField(blank=True, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='comun.Product')),
            ],
        ),
    ]
