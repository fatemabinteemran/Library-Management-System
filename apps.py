#myapp_apps.py
from django.apps import AppConfig
#from django.contrib.admin.apps import AdminConfig

#class MyappAdminConfig(AdminConfig):
    #default_site = 'myapp.admin.MyappAdminArea'

class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'


