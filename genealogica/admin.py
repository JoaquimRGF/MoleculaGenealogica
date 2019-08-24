from django.contrib import admin
from .models import Person, Family
from .forms import FamilyForm

# Register your models here.


class FamilyAdmin(admin.ModelAdmin):
    form = FamilyForm
    
    
admin.site.register(Person)
admin.site.register(Family, FamilyAdmin)
