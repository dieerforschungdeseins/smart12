# Generated by Django 4.1.7 on 2024-06-13 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0004_rename_image1_place_image_remove_place_image2'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Registration',
            new_name='Registr',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='name',
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='first.place')),
                ('user_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='first.userinfo')),
            ],
        ),
    ]
