from django.contrib import admin
from .models import Profile, Case


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    pass
# Register your models here.
