# Generated by Django 4.1.5 on 2023-01-26 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0005_alter_post_offer_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='offer_type',
            field=models.CharField(choices=[('Select Offer Type', (('Summer Internship', 'Summer Internship'), ('Winter Internship Only', 'Winter Internship Only'), ('Job Only', 'Job Only'), ('Winter Internship and Job', 'Winter Internship and Job')))], default='Select Offer Type', max_length=30),
        ),
    ]
