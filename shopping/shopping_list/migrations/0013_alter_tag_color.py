# Generated by Django 4.1.3 on 2023-02-22 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shopping_list", "0012_alter_tag_color"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tag",
            name="color",
            field=models.CharField(max_length=50),
        ),
    ]
