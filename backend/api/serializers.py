from datetime import date, datetime

from rest_framework import serializers

from .models import Agenda, Consulta, Especialidade, Medico


class EspecialidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidade
        fields = "__all__"


class MedicoSerializer(serializers.ModelSerializer):
    especialidade = EspecialidadeSerializer()

    class Meta:
        model = Medico
        fields = ["id", "crm", "nome", "especialidade"]


class AgendaSerializer(serializers.ModelSerializer):
    medico = MedicoSerializer()
    horarios = serializers.SerializerMethodField()

    def get_horarios(self, obj):
        hora_atual = datetime.now()
        # Se for um dia futuro, retorne todos os horarios
        if obj.dia > date.today():
            return obj.horarios.all().values_list("horario", flat=True)
        # Se for o dia de hoje, remove os horários que já passaram
        return [obj.horarios.filter(horario__gte=hora_atual).values_list("horario", flat=True)]

    class Meta:
        model = Agenda
        fields = ["id", "medico", "dia", "horarios"]


class CriaConsultaSerializer(serializers.Serializer):
    agenda_id = serializers.IntegerField()
    horario = serializers.TimeField()

    def validate(self, data):
        "# Valida a inserção de uma Consulta"
        try:
            agenda = Agenda.objects.get(pk=data["agenda_id"])

            "# Valida data e horario da consulta"
            if agenda.dia < date.today():
                raise serializers.ValidationError("Dia de consulta invalido!")
            if agenda.dia == date.today() and data["horario"] < datetime.now().time():
                raise serializers.ValidationError("Horario de consulta invalido!")

            "# Verifica se o usuário já não possui uma consulta marcada para esse mesmo dia/hora"
            usuario = self.context["request"].user
            if (
                len(
                    Consulta.objects.filter(
                        usuario=usuario, dia=agenda.dia, horario=data["horario"]
                    )
                )
                != 0
            ):
                raise serializers.ValidationError(
                    "usuario já possui uma consulta marcada nesse horario e dia!"
                )

            "# Valida o horário da consulta"
            if (
                len(
                    Agenda.objects.filter(
                        pk=data["agenda_id"], horarios__contains=[data["horario"]]
                    )
                )
                == 0
            ):
                raise serializers.ValidationError("Horario indisponível!")

        except Agenda.DoesNotExist:
            raise serializers.ValidationError("O id da agenda não existe!")
        return data

    def create(self, validated_data):
        horario = validated_data["horario"]
        agenda = Agenda.objects.get(pk=validated_data["agenda_id"])
        medico = agenda.medico
        dia = agenda.dia
        usuario = self.context["request"].user
        return Consulta.objects.create(dia=dia, horario=horario, usuario=usuario, medico=medico)


"""
{
  "id": 2,
  "dia": "2020-03-01",
  "horario": "09:00",
  "data_agendamento": "2020-02-01T10:45:0-03:00",
  "medico": {
    "id": 1,
    "crm": 3711,
    "nome": "Drauzio Varella",
    "especialidade": {
            "id":2,
            "nome": "Pediatria"
        }
  }
}
"""


class ConsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consulta
        fields = "__all__"
