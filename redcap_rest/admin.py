from django.contrib import admin

from .models import LabResult, Identity, Mrn

admin.site.register(LabResult)
admin.site.register(Identity)
admin.site.register(Mrn)
