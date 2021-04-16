from django.db.models import Q
from rest_framework import mixins, viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    EspecialidadeSerializer,
    MedicoSerializer,
    AgendaSerializer
)
from .models import Especialidade, Medico, Agenda


'#  Funcao para criar uma query com a condicao Or sobre a lista array'


def build_or_query(array, field):
    query = Q()
    for item in array:
        query |= Q(**{field: item})

    return query


class EspecialidadeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Especialidade.objects.all()
    serializer_class = EspecialidadeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['^nome']


class MedicoViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = MedicoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Medico.objects.all()
        nome_filter = self.request.query_params.get('search', None)
        especialidade_filter_list = self.request.query_params.getlist('especialidade', None)

        if nome_filter:
            queryset = queryset.filter(Q(nome__istartswith=nome_filter))
        if especialidade_filter_list:
            query = build_or_query(especialidade_filter_list, 'especialidade')
            queryset = queryset.filter(query)

        return queryset


class AgendaViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = AgendaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Agenda.objects.all()
        medico_filter_list = self.request.query_params.getlist('medico', None)
        especialidade_filter_list = self.request.query_params.getlist('especialidade', None)
        data_inicio_filter = self.request.query_params.get('data_inicio', None)
        data_final_filter = self.request.query_params.get('data_final', None)

        if medico_filter_list:
            query_medico = build_or_query(medico_filter_list, 'medico__id')
            queryset = queryset.filter(query_medico)
        if especialidade_filter_list:
            query_especialidade = build_or_query(especialidade_filter_list, 'medico__especialidade')
            queryset = queryset.filter(query_especialidade)
        if data_final_filter and data_final_filter:
            queryset = queryset.filter(dia__range=[data_inicio_filter, data_final_filter])
            
        return queryset
