# Generated by Django 4.1.5 on 2023-01-26 20:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0008_alter_post_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
    ]
