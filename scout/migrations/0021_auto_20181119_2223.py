# Generated by Django 2.0.7 on 2018-11-19 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scout', '0020_auto_20181119_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message',
            field=models.TextField(blank=True, default=None, max_length=2000, null=True, verbose_name='Message'),
        ),
    ]
