# Generated by Django 2.0.7 on 2018-09-05 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scout', '0004_auto_20180903_1433'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=200, null=True, verbose_name='Name')),
                ('email', models.CharField(blank=True, default=None, max_length=200, null=True, verbose_name='Email')),
                ('message', models.CharField(blank=True, default=None, max_length=2000, null=True, verbose_name='Message')),
            ],
        ),
    ]
