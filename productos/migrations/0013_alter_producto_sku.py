# Generated by Django 4.1.7 on 2023-03-02 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0012_alter_producto_sku'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='sku',
            field=models.IntegerField(default=77201043, primary_key=True, serialize=False),
        ),
    ]