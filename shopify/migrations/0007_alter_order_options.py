# Generated by Django 5.2.1 on 2025-05-29 08:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopify', '0006_alter_orderitem_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-created_at'], 'verbose_name': 'Order', 'verbose_name_plural': 'Orders'},
        ),
    ]
