from django.contrib import admin
from models_app.models import User,Startup,GovernmentAgency,Investor

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email','role']
    list_filter = ['email','role']
    search_fields = ['email',]

admin.site.register(User,UserAdmin)


class StartUpAdmin(admin.ModelAdmin):
    list_display = ['id','owner','startup_name','registration_number']
    search_fields = ['startup_name','registration_number']

admin.site.register(Startup,StartUpAdmin)


class GovernmentAgencyAdmin(admin.ModelAdmin):
    list_display = ['id','user','agency_name']
    search_fields = ['agency_name']
    
admin.site.register(GovernmentAgency,GovernmentAgencyAdmin)

class InvestorAdmin(admin.ModelAdmin):
    list_display = ['id','user','investment_focus']
    search_fields = ['user.first_name','user.last_name','investment_focus']

admin.site.register(Investor,InvestorAdmin)
