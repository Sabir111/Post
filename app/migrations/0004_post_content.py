# Generated by Django 2.2.3 on 2019-07-15 07:54

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_post_view_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='content',
            field=tinymce.models.HTMLField(default=1),
            preserve_default=False,
        ),
    ]
