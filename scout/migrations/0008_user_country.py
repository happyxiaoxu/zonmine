# Generated by Django 2.0.7 on 2018-10-11 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scout', '0007_auto_20180918_0052'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='country',
            field=models.CharField(choices=[('1', 'USA'), ('2', 'UK'), ('3', 'FR')], default='2', max_length=1, verbose_name='Country'),
        ),
    ]
