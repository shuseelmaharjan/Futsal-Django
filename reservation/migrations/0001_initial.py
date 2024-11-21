# Generated by Django 5.1 on 2024-11-20 18:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('futsal', '0004_alter_futsal_latitude_alter_futsal_longitude'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('booking_date', models.DateField()),
                ('is_confirmed', models.BooleanField(blank=True, default=False, null=True)),
                ('is_reserved', models.BooleanField(blank=True, default=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(blank=True, default=False, null=True)),
                ('futsal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='futsal.futsal')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
