from django.contrib import admin
from .models import Especialidade, Medico, Agenda

# Register your models here.
admin.site.register(Especialidade)
admin.site.register(Medico)
admin.site.register(Agenda)
