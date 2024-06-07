# Generated by Django 5.0.6 on 2024-06-07 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('party', '0016_entry_team_member_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='exits_automatically',
            field=models.BooleanField(blank=True, help_text='If not, we will try our best to guess where it ends/loops.', null=True),
        ),
        migrations.AddField(
            model_name='entry',
            name='has_audio',
            field=models.BooleanField(blank=True, help_text='If we don’t hear anything, is it a problem?', null=True),
        ),
        migrations.AddField(
            model_name='entry',
            name='platform',
            field=models.CharField(choices=[('WEB', 'Chromium + web server'), ('LIN', 'Linux'), ('WIN', 'Windows (Proton)'), ('OTH', 'Other (specify below)')], default='LIN', max_length=3),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='entry',
            name='contact_phone',
            field=models.CharField(blank=True, help_text='We will contact you if we have issues testing that your demo works or if you win something and don’t show up to the award ceremony.', max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='entry',
            name='instructions',
            field=models.TextField(blank=True, help_text='Should we press some button after opening your demo? Anything you want to clarify about the above? If you are not sure, feel free to ask from the organizers.', null=True),
        ),
    ]