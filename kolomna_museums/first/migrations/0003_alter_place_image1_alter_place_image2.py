# Generated by Django 4.1.7 on 2024-06-12 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0002_rename_image_place_image1_place_image2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='image1',
            field=models.FileField(null=True, upload_to='static/logo_place'),
        ),
        migrations.AlterField(
            model_name='place',
            name='image2',
            field=models.FileField(null=True, upload_to='static/logo_place'),
        ),
    ]