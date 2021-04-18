from django.contrib import admin

from .models import Agenda, Especialidade, Horario, Medico

# Register your models here.
admin.site.register(Especialidade)
admin.site.register(Medico)
admin.site.register(Horario)


class AgendaAdmin(admin.ModelAdmin):
    list_display = ("medico", "dia", "get_horarios")
    list_filter = ("medico", "dia")

    @admin.display(description="Horários")
    def get_horarios(self, obj):
        return ", ".join(i.isoformat() for i in obj.horarios.values_list("horario", flat=True))


admin.site.register(Agenda, AgendaAdmin)
