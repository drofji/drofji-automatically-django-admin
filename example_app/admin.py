from django.contrib import admin
from example_app import models
from drofji_automatically_django_admin.models import AutoAdminModel

AutoAdminModel.register_all_admins()

