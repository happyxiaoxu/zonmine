# Generated by Django 2.0.7 on 2018-09-03 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scout', '0003_auto_20180903_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='job_id',
            field=models.CharField(blank=True, default=None, max_length=200, null=True, verbose_name='Job Id'),
        ),
    ]