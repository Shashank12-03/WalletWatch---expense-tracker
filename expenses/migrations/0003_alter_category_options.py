# Generated by Django 4.2.7 on 2024-01-15 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0002_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
    ]
