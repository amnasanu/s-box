# Generated by Django 4.1 on 2022-08-28 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_payment_payment_signature_payment_razorpay_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_total',
            field=models.IntegerField(),
        ),
    ]
