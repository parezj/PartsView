# Generated by Django 2.1.3 on 2018-12-10 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0002_auto_20181209_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='desc',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
