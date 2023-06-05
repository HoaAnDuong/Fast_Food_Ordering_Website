from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Complaint)
admin.site.register(Complaint_Status)
admin.site.register(Moderator_Changelog)
admin.site.register(Action)