# Generated by Django 5.0.6 on 2024-06-07 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('party', '0017_entry_exits_automatically_entry_has_audio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='sub_file',
            field=models.FileField(blank=True, upload_to='entries/'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='thumbnail',
            field=models.FileField(blank=True, help_text='Recommended 1920x1080 or 1280x720', upload_to='thumbnails/'),
        ),
    ]
