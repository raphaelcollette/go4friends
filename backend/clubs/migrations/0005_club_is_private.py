# Generated by Django 5.2 on 2025-04-24 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0004_delete_clubpost'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
    ]
