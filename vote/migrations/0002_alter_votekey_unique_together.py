# Generated by Django 5.0.6 on 2024-05-19 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('party', '0003_remove_party_submission_deadline_and_more'),
        ('vote', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='votekey',
            unique_together={('party', 'key')},
        ),
    ]
