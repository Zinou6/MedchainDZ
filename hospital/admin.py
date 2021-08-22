from django.contrib import admin
from .models import Doctor,Patient,Appointment,PatientDischargeDetails
from django.contrib.auth.models import User


# Register your models here.
'''
class profileAdmin(admin.TabularInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    inlines = [profileAdmin]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
'''
class DoctorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Doctor, DoctorAdmin)

class PatientAdmin(admin.ModelAdmin):
    pass
admin.site.register(Patient, PatientAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Appointment, AppointmentAdmin)

class PatientDischargeDetailsAdmin(admin.ModelAdmin):
    pass
admin.site.register(PatientDischargeDetails, PatientDischargeDetailsAdmin)

