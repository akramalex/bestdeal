# Generated by Django 5.1.2 on 2025-01-30 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactmessage',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]
