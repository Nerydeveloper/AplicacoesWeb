# Generated by Django 4.1.7 on 2023-06-13 22:30

import Weblist.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Weblist', '0018_produto_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=Weblist.models.upload_image_produto),
        ),
    ]
