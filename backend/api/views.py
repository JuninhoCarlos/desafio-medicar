from datetime import datetime, date
from django.db.models import Q
from rest_framework import mixins, viewsets, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_rw_serializers import generics

from .serializers import (
    EspecialidadeSerializer,
    MedicoSerializer,
    AgendaSerializer,
    CriaConsultaSerializer,
    ConsultaSerializer
)
from .models import Especialidade, Medico, Agenda, Consulta
from .helpers import build_or_query


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
        # Remove agendas de datas passadas da listagem
        queryset = Agenda.objects.filter(dia__gte=date.today())

        # Filtra os horarios invalidos do dia de hoje
        novo_queryset = []
        for agenda in queryset:
            # Verifico se a agenda é de hoje 
            if(agenda.dia != date.today()):
                novo_queryset.append(agenda)
                continue
            novos_horarios = []
            for hora in agenda.horarios:
                # Verifica se o horario não passou
                if hora < datetime.now().time():                    
                    continue
                novos_horarios.append(hora)
            agenda.horarios = novos_horarios
            novo_queryset.append(agenda)

        queryset = novo_queryset

        lista_filtro_medico = self.request.query_params.getlist('medico', None)
        lista_filtro_especialidade = self.request.query_params.getlist('especialidade', None)
        filtro_data_inicio = self.request.query_params.get('data_inicio', None)
        filtro_data_final = self.request.query_params.get('data_final', None)

        if lista_filtro_medico:
            query_medico = build_or_query(lista_filtro_medico, 'medico__id')
            queryset = queryset.filter(query_medico)
        if lista_filtro_especialidade:
            query_especialidade = build_or_query(lista_filtro_especialidade, 'medico__especialidade')
            queryset = queryset.filter(query_especialidade)
        if filtro_data_inicio and filtro_data_final:
            queryset = queryset.filter(dia__range=[filtro_data_inicio, filtro_data_final])

        return queryset


class ConsultaViewSet(generics.ListCreateAPIView):
    queryset = Consulta.objects.all()
    write_serializer_class = CriaConsultaSerializer
    read_serializer_class = ConsultaSerializer
    permission_classes = [IsAuthenticated]
    #def post(self,*args,**kwargs):
    #    __import__('ipdb').set_trace()
    #def create(self, request):        
        #serializer = CriaConsultaSerializer(data=request.data, context={'usuario': request.user})        
        #serializer.is_valid(raise_exception=True)
        #serializer.save()
       # return Response(serializer.data)
