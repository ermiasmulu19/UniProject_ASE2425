# Generated by Django 5.1.3 on 2024-11-30 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_merge_20241121_1855'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='duck',
            name='owners',
        ),
        migrations.RemoveField(
            model_name='duck',
            name='description',
        ),
        migrations.DeleteModel(
            name='UserDuck',
        ),
    ]
