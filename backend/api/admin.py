from django.contrib import admin
from .models import Especialidade, Medico, Horario, Agenda

# Register your models here.
admin.site.register(Especialidade)
admin.site.register(Medico)
admin.site.register(Horario)
admin.site.register(Agenda)
