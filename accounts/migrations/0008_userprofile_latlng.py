# Generated by Django 4.1.3 on 2022-11-23 07:44

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_leaveapplication_reason_leaveapplication_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='latlng',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
    ]
