# Generated by Django 3.0.6 on 2020-08-04 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports_management', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='diagnostc',
            new_name='diagnostic',
        ),
    ]
