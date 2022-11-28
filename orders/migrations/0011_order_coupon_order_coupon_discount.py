# Generated by Django 4.1.3 on 2022-11-28 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("carts", "0007_coupon_created_date_coupon_expiry_date_and_more"),
        ("orders", "0010_alter_order_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="coupon",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="carts.coupon",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="coupon_discount",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]