# Generated by Django 3.0 on 2021-01-30 06:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_book_trip'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tourist',
            old_name='fname',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='tourist',
            name='lname',
        ),
    ]
