from django.db import models
from django.contrib.auth.models import AbstractUser
from models_app.manager import UserManager
# Create your models here.

class User(AbstractUser):
    first_name = models.CharField(max_length=150, blank=True,null=False)
    last_name = models.CharField( max_length=150, blank=True,null=False)
    contact_number = models.CharField(max_length=12,null=True,blank=True)
    email = models.EmailField(unique=True,null=False,blank=False)
    role = models.CharField(max_length=20, choices=[('Startup', 'Startup'), ('Investor', 'Investor'), ('Government', 'Government'), ('Public', 'Public')])
    created_by =  models.ForeignKey('self', on_delete=models.CASCADE, related_name="user_created_by",null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    deleted_by = models.ForeignKey('self',related_name="user_deleted_by", on_delete=models.CASCADE,null=True,blank=True)
    is_deleted = models.BooleanField(default=False ,null=True, blank=True)
    deleted_on = models.DateTimeField(null=True, blank=True)

    # REQUIRED_FIELDS = ['email']
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return f'{self.id} , {self.email}'


class Startup(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE,null=False, blank=False)
    startup_name = models.CharField(max_length=100, null=False, blank=False)
    startup_description = models.TextField(null=True, blank=True)
    industry_sector = models.CharField(max_length=50, null=True, blank=True)
    founding_date = models.DateField(null=True, blank=True)
    founder_bio = models.TextField(null=True, blank=True)
    website_url = models.URLField(null=True, blank=True)
    registration_number = models.CharField(max_length=20, unique=True, null=False, blank=False)
    contact_person = models.CharField(max_length=150, null=True, blank=True)
    contact_number = models.CharField(max_length=12, null=True, blank=True)
    banner_image = models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.startup_name


class GovernmentAgency(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    agency_name = models.CharField(max_length=100, null=False, blank=False)
    agency_description = models.TextField(null=True, blank=True)
    contact_person = models.CharField(max_length=150, null=True, blank=True)
    contact_number = models.CharField(max_length=12, null=True, blank=True)

    # Additional fields for government agencies

    def __str__(self):
        return self.agency_name

class Investor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    investor_description = models.TextField(null=True, blank=True)
    investment_focus = models.CharField(max_length=100, null=True, blank=True)
    contact_person = models.CharField(max_length=150, null=True, blank=True)
    contact_number = models.CharField(max_length=12, null=True, blank=True)

    # Additional fields for investors

    def __str__(self):
        return self.user
