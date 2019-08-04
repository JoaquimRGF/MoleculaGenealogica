from django.contrib import admin
from .models import Person, Union, Family
# Register your models here.

admin.site.register(Person)
admin.site.register(Union)
admin.site.register(Family)
