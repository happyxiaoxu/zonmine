# Generated by Django 2.0.7 on 2018-09-03 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scout', '0002_auto_20180903_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='job_id',
            field=models.CharField(blank=True, default=None, max_length=200, null=True, unique=True, verbose_name='Job Id'),
        ),
    ]
