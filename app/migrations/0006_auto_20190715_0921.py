# Generated by Django 2.2.3 on 2019-07-15 09:21

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20190715_0920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=tinymce.models.HTMLField(),
        ),
    ]
