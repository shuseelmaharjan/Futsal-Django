# Generated by Django 5.1 on 2024-11-20 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='is_reserved',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
