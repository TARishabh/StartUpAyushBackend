sabse pehle folder banao, 
phir pip install virtualenv
phir python -m virtualenv <nameOfEnv>
activate karo env ko, c:/Users/test/scrapping/scrapenv/Scripts/Activate.ps1
pip install django
pip install django-rest-framework
django-admin startproject <PROJECTNAME> .
django-admin startapp <APPNAME>

the flow of django is:
settings->models->admin->serializers->views->routers(if routers are present)->urls

settings me jaake rest_framework aur app ka naam likh dena.

if setting your own custom User table, steps which need to be followed are:
settings me jaake ye likhdo:
AUTH_USER_MODEL = 'models_app.User'


phir custom models ke liye custom manager banana padta hai, vo banao