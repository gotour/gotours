# Generated by Django 3.0 on 2021-01-29 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_destinations_destinations_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='destinations',
            name='destinations_d_image1',
            field=models.ImageField(default='', upload_to='images/'),
        ),
        migrations.AddField(
            model_name='destinations',
            name='destinations_d_image2',
            field=models.ImageField(default='', upload_to='images/'),
        ),
        migrations.AddField(
            model_name='destinations',
            name='destinations_d_image3',
            field=models.ImageField(default='', upload_to='images/'),
        ),
    ]
