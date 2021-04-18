from datetime import date

from drf_rw_serializers import generics
from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .filters import AgendaFilter, MedicoFilter
from .models import Agenda, Consulta, Especialidade, Medico
from .serializers import (
    AgendaSerializer,
    ConsultaReadSerializer,
    ConsultaWriteSerializer,
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
    # Remove datas passadas da Listagem
    queryset = Agenda.objects.filter(dia__gte=date.today()).distinct()
    filterset_class = AgendaFilter


class ConsultaAPIView(generics.ListCreateAPIView):
    queryset = Consulta.objects.all()
    write_serializer_class = ConsultaWriteSerializer
    read_serializer_class = ConsultaReadSerializer
    permission_classes = [IsAuthenticated]
    # def post(self,*args,**kwargs):
    #    __import__('ipdb').set_trace()
    # def create(self, request):
    # serializer = CriaConsultaSerializer(data=request.data, context={'usuario': request.user})
    # serializer.is_valid(raise_exception=True)
    # serializer.save()
    # return Response(serializer.data)
