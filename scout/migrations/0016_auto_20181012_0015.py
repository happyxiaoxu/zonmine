# Generated by Django 2.0.7 on 2018-10-11 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scout', '0015_auto_20181012_0011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='country',
            field=models.CharField(choices=[('CA', 'Canada'), ('FR', 'France'), ('DE', 'Germany'), ('IT', 'Italy'), ('SP', 'Spain'), ('UK', 'United Kingdom'), ('USA', 'United States')], default='USA', max_length=20, verbose_name='Country'),
        ),
    ]