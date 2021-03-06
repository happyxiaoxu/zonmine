# Generated by Django 2.0.7 on 2018-09-17 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scout', '0006_user_subscribed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='amazon_dimensions',
            field=models.CharField(blank=True, default=None, max_length=2000, null=True, verbose_name='Amazon Product Dimensions'),
        ),
        migrations.AlterField(
            model_name='product',
            name='amazon_in_stock',
            field=models.CharField(blank=True, default=None, max_length=2000, null=True, verbose_name='Amazon Product In Stock'),
        ),
        migrations.AlterField(
            model_name='product',
            name='amazon_item_model_number',
            field=models.CharField(blank=True, default=None, max_length=2000, null=True, verbose_name='Amazon Product Model Number'),
        ),
        migrations.AlterField(
            model_name='product',
            name='amazon_manufacturer',
            field=models.CharField(blank=True, default=None, max_length=2000, null=True, verbose_name='Amazon Product Manufacturer'),
        ),
        migrations.AlterField(
            model_name='product',
            name='amazon_sold_by',
            field=models.CharField(blank=True, default=None, max_length=2000, null=True, verbose_name='Amazon Product Sold By'),
        ),
        migrations.AlterField(
            model_name='product',
            name='amazon_weight',
            field=models.CharField(blank=True, default=None, max_length=2000, null=True, verbose_name='Amazon Product Weight'),
        ),
    ]
