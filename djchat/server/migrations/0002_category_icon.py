# Generated by Django 5.1.2 on 2024-11-09 09:44

import server.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='icon',
            field=models.FileField(blank=True, null=True, upload_to=server.models.category_icon_upload_path),
        ),
    ]
