# Generated by Django 4.1.7 on 2023-05-10 12:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0005_remove_payment_status_mobile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment_status',
            old_name='cart_id',
            new_name='order_id',
        ),
    ]
