# Generated by Django 4.1.7 on 2024-06-12 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='place',
            old_name='image',
            new_name='image1',
        ),
        migrations.AddField(
            model_name='place',
            name='image2',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]
