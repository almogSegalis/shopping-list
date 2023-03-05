# Generated by Django 4.1.3 on 2023-03-01 10:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("shopping_list", "0019_delete_order"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("order_time", models.DateTimeField()),
                ("order_num", models.CharField(default="", max_length=100)),
                ("items", models.ManyToManyField(to="shopping_list.item")),
                (
                    "venue_name",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="shopping_list.tag",
                    ),
                ),
            ],
        ),
    ]