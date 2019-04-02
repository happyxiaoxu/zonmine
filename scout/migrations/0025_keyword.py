# Generated by Django 2.1.2 on 2019-04-01 03:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scout', '0024_auto_20190331_1846'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(blank=True, default=None, max_length=2000, null=True, verbose_name='Keyword')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scout.Job')),
            ],
        ),
    ]
