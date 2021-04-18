from datetime import date

from drf_rw_serializers import generics
from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .filters import MedicoFilter
from .models import Agenda, Consulta, Especialidade, Medico
from .serializers import (
    AgendaSerializer,
    ConsultaSerializer,
    CriaConsultaSerializer,
    EspecialidadeSerializer,
    MedicoSerializer,
)


class EspecialidadeAPIView(ListAPIView):
    queryset = Especialidade.objects.all()
    serializer_class = EspecialidadeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["^nome"]


class MedicoAPIView(ListAPIView):
    serializer_class = MedicoSerializer
    permission_classes = [IsAuthenticated]
    queryset = Medico.objects.all()
    filterset_class = MedicoFilter


class AgendaAPIView(ListAPIView):
    serializer_class = AgendaSerializer
    permission_classes = [IsAuthenticated]
    queryset = Agenda.objects.filter(dia__gte=date.today()).distinct()

    # def get_queryset(self):
    # Remove agendas de datas passadas da listagem

    # lista_filtro_medico = self.request.query_params.getlist("medico", None)
    # lista_filtro_especialidade = self.request.query_params.getlist("especialidade", None)
    # filtro_data_inicio = self.request.query_params.get("data_inicio", None)
    # filtro_data_final = self.request.query_params.get("data_final", None)

    # if lista_filtro_medico:
    #    query_medico = build_or_query(lista_filtro_medico, "medico__id")
    #    queryset = queryset.filter(query_medico)
    # if lista_filtro_especialidade:
    #    query_especialidade = build_or_query(
    #        lista_filtro_especialidade, "medico__especialidade"
    #    )
    #    queryset = queryset.filter(query_especialidade)
    # if filtro_data_inicio and filtro_data_final:
    #    queryset = queryset.filter(dia__range=[filtro_data_inicio, filtro_data_final])

    #    return queryset


class ConsultaAPIView(generics.ListCreateAPIView):
    queryset = Consulta.objects.all()
    write_serializer_class = CriaConsultaSerializer
    read_serializer_class = ConsultaSerializer
    permission_classes = [IsAuthenticated]
    # def post(self,*args,**kwargs):
    #    __import__('ipdb').set_trace()
    # def create(self, request):
    # serializer = CriaConsultaSerializer(data=request.data, context={'usuario': request.user})
    # serializer.is_valid(raise_exception=True)
    # serializer.save()
    # return Response(serializer.data)
