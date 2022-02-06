# Generated by Django 3.2 on 2022-02-02 12:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_rename_quality_product_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcategory',
            name='discount',
            field=models.PositiveIntegerField(blank=True, default=0, validators=[django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='is_active',
            field=models.BooleanField(db_index=True, default=True),
        ),
    ]