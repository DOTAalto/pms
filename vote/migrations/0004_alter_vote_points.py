# Generated by Django 5.0.6 on 2024-05-27 17:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0003_vote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='points',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(5)]),
        ),
    ]
