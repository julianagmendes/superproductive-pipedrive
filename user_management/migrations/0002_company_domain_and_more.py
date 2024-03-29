# Generated by Django 4.2.6 on 2023-12-11 01:36

from django.db import migrations, models
import django.db.models.deletion
import django_tenants.postgresql_backend.base


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schema_name', models.CharField(db_index=True, max_length=63, unique=True, validators=[django_tenants.postgresql_backend.base._check_schema_name])),
                ('name', models.CharField(max_length=100, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('company_type', models.CharField(choices=[('tech', 'Technology'), ('finance', 'Finance'), ('healthcare', 'Healthcare'), ('manufacturing', 'Manufacturing'), ('energy', 'Energy'), ('media', 'Entertainment and Media'), ('real_estate', 'Real Estate'), ('legal_services', 'Legal and Professional Services'), ('consulting', 'Consulting'), ('food_beverage', 'Food and Beverage'), ('pharmaceutical', 'Pharmaceutical or Biotechnology'), ('environmental', 'Environmental Services'), ('other', 'Other')], default='other', max_length=15)),
                ('custom_company_type', models.CharField(blank=True, max_length=100, null=True)),
                ('company_size', models.CharField(choices=[('small', 'Small (1-50 employees)'), ('medium', 'Medium (51-500 employees)'), ('large', 'Large (501+ employees)')], default='small', max_length=10)),
                ('pm_platform', models.CharField(choices=[('asana', 'Asana'), ('jira', 'Jira')], default='asana', max_length=20)),
                ('communication_platform', models.CharField(choices=[('teams', 'Microsoft Teams'), ('slack', 'Slack')], default='teams', max_length=20)),
                ('file_platform', models.CharField(choices=[('dropbox', 'Dropbox'), ('sharepoint', 'SharePoint'), ('google_drive', 'Google Drive')], default='sharepoint', max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(db_index=True, max_length=253, unique=True)),
                ('is_primary', models.BooleanField(db_index=True, default=True)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='domains', to='user_management.company')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='platformrequirement',
            name='platform_integration',
        ),
        migrations.RemoveField(
            model_name='userplatformintegration',
            name='platform_integration',
        ),
        migrations.RemoveField(
            model_name='userplatformintegration',
            name='requirements',
        ),
        migrations.RemoveField(
            model_name='userplatformintegration',
            name='user_profile',
        ),
        migrations.RemoveField(
            model_name='userplatformparameters',
            name='platform_requirement',
        ),
        migrations.RemoveField(
            model_name='userplatformparameters',
            name='user_platform_integration',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='selected_platforms',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='subscription_plan',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='Platform',
        ),
        migrations.DeleteModel(
            name='PlatformRequirement',
        ),
        migrations.DeleteModel(
            name='SubscriptionPlan',
        ),
        migrations.DeleteModel(
            name='UserPlatformIntegration',
        ),
        migrations.DeleteModel(
            name='UserPlatformParameters',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
