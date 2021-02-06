# Generated by Django 3.0 on 2021-01-29 09:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20210129_0935'),
    ]

    operations = [
        migrations.CreateModel(
            name='book_trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trip_date', models.CharField(max_length=100)),
                ('adult', models.CharField(max_length=100)),
                ('destinations', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Destinations')),
                ('tourist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Tourist')),
            ],
        ),
    ]
