# Generated by Django 5.2 on 2025-05-22 08:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_alter_material_material_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='couse',
            options={'ordering': ['-created_at']},
        ),
    ]
