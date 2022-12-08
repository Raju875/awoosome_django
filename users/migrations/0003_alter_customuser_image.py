# Generated by Django 4.1.2 on 2022-10-30 11:27

from django.db import migrations, models
import utils.image


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to=utils.image.file_upload),
        ),
    ]
