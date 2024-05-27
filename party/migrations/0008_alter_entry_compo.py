# Generated by Django 5.0.6 on 2024-05-27 17:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('party', '0007_compo_voting_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='compo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='party.compo'),
        ),
    ]
