# Generated by Django 5.0 on 2024-02-05 23:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('user_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('template_name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('file_id', models.CharField(blank=True, max_length=255, null=True)),
                ('folder_id', models.CharField(blank=True, max_length=255, null=True)),
                ('subject', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_management.company')),
                ('platform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.platformintegration')),
            ],
        ),
    ]
