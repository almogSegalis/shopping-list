# Generated by Django 4.1.3 on 2023-03-05 10:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shopping_list", "0024_item_updated_at"),
    ]

    operations = [
        migrations.RenameField(
            model_name="item",
            old_name="date",
            new_name="created_at",
        ),
    ]
