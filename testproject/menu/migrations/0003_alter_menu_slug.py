# Generated by Django 4.1.1 on 2025-05-15 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_alter_menu_options_alter_menuitem_options_menu_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='slug',
            field=models.SlugField(null=True, unique=True, verbose_name='Menu Slug'),
        ),
    ]