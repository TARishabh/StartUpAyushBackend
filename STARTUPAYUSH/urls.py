"""
URL configuration for STARTUPAYUSH project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from models_app.views import (
    LoginUser,
    RegisterUser,
    StartUpViewset,
    GovernmentAgencyViewset,
    InvestorViewset,
    )
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'startup',StartUpViewset)
router.register(r'agency',GovernmentAgencyViewset)
router.register(r'investor',InvestorViewset)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login_user/',LoginUser.as_view()),
    path('register_user/', RegisterUser.as_view({'post':'create'})),
    path('api/', include(router.urls))
]

# consider create function for now only, the incoming data will be in form of:
# {}