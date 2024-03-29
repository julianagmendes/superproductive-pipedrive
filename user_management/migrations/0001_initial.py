# Generated by Django 4.2.6 on 2023-10-29 21:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('category', models.CharField(choices=[('communication', 'Communication'), ('program_management', 'Program Management'), ('e_sign', 'E-Sign'), ('main_automation_ui', 'Main Automation UI')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='PlatformRequirement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('platform_integration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_management.platform')),
            ],
        ),
        migrations.CreateModel(
            name='SubscriptionPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='UserPlatformIntegration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform_integration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_management.platform')),
                ('requirements', models.ManyToManyField(to='user_management.platformrequirement')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=255)),
                ('is_subscribed', models.BooleanField(default=False)),
                ('selected_platforms', models.ManyToManyField(to='user_management.platform')),
                ('subscription_plan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user_management.subscriptionplan')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserPlatformParameters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255)),
                ('platform_requirement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_management.platformrequirement')),
                ('user_platform_integration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_management.userplatformintegration')),
            ],
        ),
        migrations.AddField(
            model_name='userplatformintegration',
            name='user_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_platform_integrations', to='user_management.userprofile'),
        ),
    ]
