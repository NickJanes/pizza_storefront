# Generated by Django 3.1 on 2020-09-29 10:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_auto_20200929_0304'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='productType',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.producttype'),
        ),
    ]