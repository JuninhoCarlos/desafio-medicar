from django.contrib import admin

from .models import Agenda, Especialidade, Horario, Medico


class AgendaAdmin(admin.ModelAdmin):
    list_display = ["pk", "medico", "dia", "get_horarios"]
    list_filter = ["medico", "dia"]

    @admin.display(description="Horários")
    def get_horarios(self, obj):
        return ", ".join(i.isoformat() for i in obj.horarios.values_list("horario", flat=True))


class MedicoAdmin(admin.ModelAdmin):
    list_display = ["pk", "nome", "crm", "especialidade"]
    list_filter = ["nome", "especialidade"]


admin.site.register(Medico, MedicoAdmin)
admin.site.register(Agenda, AgendaAdmin)
admin.site.register(Especialidade)
admin.site.register(Horario)
