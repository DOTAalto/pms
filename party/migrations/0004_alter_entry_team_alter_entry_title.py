# Generated by Django 5.0.6 on 2024-05-24 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('party', '0003_remove_party_submission_deadline_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='team',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='entry',
            name='title',
            field=models.CharField(max_length=32),
        ),
    ]
