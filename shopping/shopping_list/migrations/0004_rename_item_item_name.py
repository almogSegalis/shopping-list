# Generated by Django 4.1.3 on 2023-02-20 10:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shopping_list", "0003_rename_items_item"),
    ]

    operations = [
        migrations.RenameField(
            model_name="item",
            old_name="item",
            new_name="name",
        ),
    ]
