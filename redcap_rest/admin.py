from django.contrib import admin

from .models import LabResult, Identity, Mrn, Project

admin.site.register(LabResult)
admin.site.register(Identity)
admin.site.register(Mrn)
admin.site.register(Project)



