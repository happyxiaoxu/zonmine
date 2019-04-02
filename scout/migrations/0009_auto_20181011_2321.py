# Generated by Django 2.0.7 on 2018-10-11 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scout', '0008_user_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='country',
            field=models.CharField(choices=[('1', 'CA'), ('2', 'FR'), ('3', 'DE'), ('4', 'IT'), ('5', 'SP'), ('6', 'UK'), ('7', 'USA')], default='7', max_length=1, verbose_name='Country'),
        ),
    ]
