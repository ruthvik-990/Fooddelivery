# Generated by Django 3.0 on 2020-06-21 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0005_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
