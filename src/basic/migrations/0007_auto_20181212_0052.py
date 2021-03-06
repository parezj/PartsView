# Generated by Django 2.1.3 on 2018-12-11 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0006_auto_20181211_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cat1',
            name='desc',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='cat1',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='cat1',
            name='name_pretty',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='cat2',
            name='desc',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='cat2',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='cat2',
            name='name_pretty',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='param',
            name='desc',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='param',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='param',
            name='name_pretty',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='desc',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='name_pretty',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
