# Generated by Django 5.0 on 2023-12-28 23:02

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pipedrive', '0002_alter_pipedrivewebhook_integration_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pipedrivewebhook',
            old_name='webhook_url',
            new_name='url',
        ),
        migrations.RemoveField(
            model_name='pipedrivewebhook',
            name='webhook_id',
        ),
        migrations.AddField(
            model_name='pipedrivewebhook',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pipedrivewebhook',
            name='date_last_called',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pipedrivewebhook',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='pipedrivewebhook',
            name='id',
            field=models.CharField(max_length=255, primary_key=True, serialize=False),
        ),
    ]