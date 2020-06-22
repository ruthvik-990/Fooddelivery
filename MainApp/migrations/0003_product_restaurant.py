# Generated by Django 3.0 on 2020-06-19 10:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0002_restaurant'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='restaurant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='MainApp.Restaurant'),
        ),
    ]
