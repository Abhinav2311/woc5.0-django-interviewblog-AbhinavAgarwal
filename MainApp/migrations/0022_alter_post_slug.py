# Generated by Django 4.1.5 on 2023-01-30 12:54

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0021_post_bookmarks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=autoslug.fields.AutoSlugField(blank=True, null=True),
        ),
    ]
