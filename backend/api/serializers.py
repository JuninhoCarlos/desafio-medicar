from datetime import date, datetime

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Agenda, Consulta, Especialidade, Medico


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = get_user_model()(**validated_data)
        user.set_password(password)
        user.save()
        return user


class EspecialidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidade
        fields = ["id", "nome"]


class MedicoSerializer(serializers.ModelSerializer):
    especialidade = EspecialidadeSerializer()

    class Meta:
        model = Medico
        fields = ["id", "crm", "nome", "especialidade"]


class AgendaSerializer(serializers.ModelSerializer):
    medico = MedicoSerializer()
    horarios = serializers.SerializerMethodField()

    def filtra_horarios_diponiveis(self, agenda, horario_queryset):
        horarios = []

        for horario in horario_queryset:
            if Consulta.objects.filter(agenda=agenda, horario=horario.horario).count() == 0:
                horarios.append(horario.horario)
        return horarios

    def get_horarios(self, obj):
        hora_atual = datetime.now()
        # Se for um dia futuro, retorne todos os horarios
        if obj.dia > date.today():
            return [
                hora.strftime("%H:%M")
                for hora in self.filtra_horarios_diponiveis(obj, obj.horarios.all())
            ]
        # Se for o dia de hoje, remove os horários que já passaram
        return [
            hora.strftime("%H:%M")
            for hora in self.filtra_horarios_diponiveis(
                obj, obj.horarios.filter(horario__gte=hora_atual)
            )
        ]

    class Meta:
        model = Agenda
        fields = ["id", "medico", "dia", "horarios"]


class ConsultaWriteSerializer(serializers.Serializer):
    agenda_id = serializers.IntegerField()
    horario = serializers.TimeField()

    def validate(self, data):

        "# Valida a inserção de uma Consulta"
        try:
            agenda = Agenda.objects.get(pk=data["agenda_id"])
        except Agenda.DoesNotExist as agenda_nao_existe:
            raise serializers.ValidationError("O id da agenda não existe!") from agenda_nao_existe

        "# Valida data e horario da consulta"
        if agenda.dia < date.today():
            raise serializers.ValidationError("Dia de consulta invalido!")
        if agenda.dia == date.today() and data["horario"] < datetime.now().time():
            raise serializers.ValidationError("Horario de consulta invalido!")

        "# Verifica se o usuário já não possui uma consulta marcada para esse mesmo dia/hora"
        usuario = self.context["request"].user
        if (
            Consulta.objects.filter(
                usuario=usuario, agenda__dia=agenda.dia, horario=data["horario"]
            ).count()
            != 0
        ):
            raise serializers.ValidationError(
                "usuario já possui uma consulta marcada nesse horario e dia!"
            )

        # Verifica se o horário existe na agenda
        if (
            Agenda.objects.filter(pk=data["agenda_id"], horarios__horario=data["horario"]).count()
            == 0
        ):
            raise serializers.ValidationError("Horario inexistente na agenda!")

        # Verifica se o horário não já está ocupado
        if Consulta.objects.filter(agenda=data["agenda_id"], horario=data["horario"]).count() != 0:
            raise serializers.ValidationError("Horário já está ocupado!")

        return data

    def create(self, validated_data):
        horario = validated_data["horario"]
        agenda = Agenda.objects.get(pk=validated_data["agenda_id"])
        usuario = self.context["request"].user
        return Consulta.objects.create(horario=horario, usuario=usuario, agenda=agenda)


class ConsultaReadSerializer(serializers.ModelSerializer):
    horario = serializers.TimeField(format="%H:%M")
    dia = serializers.SerializerMethodField()
    medico = serializers.SerializerMethodField()

    def get_dia(self, obj):
        return obj.agenda.dia

    def get_medico(self, obj):
        return MedicoSerializer(obj.agenda.medico).data

    class Meta:
        model = Consulta
        fields = ["id", "dia", "horario", "data_agendamento", "medico"]
