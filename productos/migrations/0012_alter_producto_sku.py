# Generated by Django 4.1.7 on 2023-03-02 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0011_alter_producto_sku'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='sku',
            field=models.IntegerField(default=13187321, primary_key=True, serialize=False),
        ),
    ]