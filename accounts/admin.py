from django.contrib import admin
from . import models

admin.site.register(models.PatientProfile)
admin.site.register(models.DoctorProfile)
admin.site.register(models.AssistantProfile)
admin.site.register(models.PatientCard)
admin.site.register(models.DoctorCard)
admin.site.register(models.TempDoctorCard)
admin.site.register(models.NessaCard)
admin.site.register(models.VascularCard)
admin.site.register(models.FavoriteMedicine)
admin.site.register(models.NessaPictures)
