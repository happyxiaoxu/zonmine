# Generated by Django 2.0.7 on 2018-09-03 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scout', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.BinaryField(blank=True, default=None, null=True, verbose_name='File')),
                ('scout_file', models.BooleanField(default=False, verbose_name='Scout File')),
                ('asin_file', models.BooleanField(default=False, verbose_name='ASIN File')),
                ('job_id', models.CharField(blank=True, default=None, max_length=200, null=True, verbose_name='Job Id')),
            ],
        ),
        migrations.RemoveField(
            model_name='job',
            name='asin_file',
        ),
        migrations.RemoveField(
            model_name='job',
            name='scout_file',
        ),
    ]
