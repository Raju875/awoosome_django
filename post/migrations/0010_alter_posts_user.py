# Generated by Django 4.1.3 on 2022-11-22 08:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0009_alter_comment_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='post', related_query_name='pq', to=settings.AUTH_USER_MODEL),
        ),
    ]
