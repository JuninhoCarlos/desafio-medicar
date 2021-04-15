from rest_framework import serializers
from .models import Especialidade, Medico, Agenda


class EspecialidadeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Especialidade
        fields = '__all__'


class MedicoSerializer(serializers.ModelSerializer):
    especialidade = EspecialidadeSerializer()

    class Meta:
        model = Medico
        fields = ['id', 'crm', 'nome', 'especialidade']


class AgendaSerializer(serializers.ModelSerializer):
    medico = MedicoSerializer()
    horarios = serializers.ListField(child=serializers.TimeField(format='%H:%M'))

    class Meta:
        model = Agenda
        fields = ['id', 'medico', 'dia', 'horarios']
        
