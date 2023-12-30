from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from django.contrib.auth.models import AbstractUser

class Company(TenantMixin):
    INDUSTRY_CHOICES = [
        ('tech', 'Technology'),
        ('finance', 'Finance'),
        ('healthcare', 'Healthcare'),
        ('manufacturing', 'Manufacturing'),
        ('energy', 'Energy'),
        ('media', 'Entertainment and Media'),
        ('real_estate', 'Real Estate'),
        ('legal_services', 'Legal and Professional Services'),
        ('consulting', 'Consulting'),
        ('food_beverage', 'Food and Beverage'),
        ('pharmaceutical', 'Pharmaceutical or Biotechnology'),
        ('environmental', 'Environmental Services'),
        ('other', 'Other'),
    ]

    SIZE_CHOICES = [
        ('small', 'Small (1-50 employees)'),
        ('medium', 'Medium (51-500 employees)'),
        ('large', 'Large (501+ employees)'),
    ]

    PM_PLATFORM_CHOICES = [
        ('asana', 'Asana'),
        ('jira', 'Jira'),
    ]

    COMM_PLATFORM_CHOICES = [
        ('teams', 'Microsoft Teams'),
        ('slack', 'Slack'),
    ]

    FILES_PLATFORM_CHOICES = [
        ('dropbox', 'Dropbox'),
        ('sharepoint', 'SharePoint'),
        ('google_drive', 'Google Drive')
    ]

    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    auto_create_schema = True

    company_type = models.CharField(
        max_length=15,
        choices=INDUSTRY_CHOICES,
        default='other',
    )
    custom_company_type = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    company_size = models.CharField(
        max_length=10,
        choices=SIZE_CHOICES,
        default='small',  # Set a default size if needed
    )

    pm_platform = models.CharField(
        max_length=20,
        choices=PM_PLATFORM_CHOICES,
        default='asana',
    )

    communication_platform = models.CharField(
        max_length=20,
        choices=COMM_PLATFORM_CHOICES,
        default='teams',
    )

    file_platform = models.CharField(
        max_length=20,
        choices=FILES_PLATFORM_CHOICES,
        default='sharepoint',
    )

    def __str__(self):
        return self.name


class Domain(DomainMixin):
    pass

# class CustomUser(AbstractUser):
#     company = models.ForeignKey(Company, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.username

# class SubscriptionPlan(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)

# class Platform(models.Model):
#     CATEGORY_CHOICES = [
#         ('communication', 'Communication'),
#         ('program_management', 'Program Management'),
#         ('e_sign', 'E-Sign'),
#         ('file_storage', 'File Storage'),

#     ]

#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

#     def __str__(self):
#         return self.name
    
# class PlatformRequirement(models.Model):
#     platform_integration = models.ManyToManyField(Platform, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     description = models.TextField()
    
# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     company_name = models.CharField(max_length=255)
#     is_subscribed = models.BooleanField(default=False)
#     subscription_plan = models.OneToOneField(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True)
#     selected_platforms = models.ManyToManyField(Platform)

# class UserPlatformIntegration(models.Model):
#     user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_platform_integrations')
#     platform_integration = models.ForeignKey(Platform, on_delete=models.CASCADE)
#     requirements = models.ManyToManyField(PlatformRequirement)

# class UserPlatformParameters(models.Model):
#     user_platform_integration = models.ForeignKey(UserPlatformIntegration, on_delete=models.CASCADE)
#     platform_requirement = models.ForeignKey(PlatformRequirement, on_delete=models.CASCADE)
#     value = models.CharField(max_length=255)

'''
# Import necessary models
from your_app.models import UserProfile, Platform, PlatformRequirement

# 1. User Registration and Profile
user_profile = UserProfile.objects.create(
    user=User.objects.create(username='johndoe', email='johndoe@example.com'),
    company_name='ABC Inc.',
    pipedrive_api_token='[John\'s Pipedrive API Token]',
    is_subscribed=True,
    subscription_plan='Business Pro'
)

# 2. Select Platforms
platform_teams = Platform.objects.get(name='Microsoft Teams')
platform_asana = Platform.objects.get(name='Asana')

# 3. Add User's Requirements for Each Platform
# Microsoft Teams
platform_teams_requirements = PlatformRequirement.objects.create(
    platform_integration=platform_teams,
    name='Microsoft Teams API Key',
    description='API Key for Microsoft Teams',
)

# Asana
platform_asana_requirements = PlatformRequirement.objects.create(
    platform_integration=platform_asana,
    name='Asana API Key',
    description='API Key for Asana',
)

# 4. Save User's Platform Requirements
user_profile.selected_platforms.add(platform_teams, platform_asana)
user_profile.userplatformintegration_set.create(requirements=platform_teams_requirements)
user_profile.userplatformintegration_set.create(requirements=platform_asana_requirements)



'''