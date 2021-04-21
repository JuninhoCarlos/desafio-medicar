from datetime import date, datetime

from django.db.models import Q
from drf_rw_serializers import generics
from rest_framework import filters
from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView
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
    filterset_class = AgendaFilter

    def get_queryset(self):
        queryset = Agenda.objects.filter(dia__gte=date.today())
        agendas_invalidas = []

        # Verifica se a agenda ainda está disponível
        for agenda in queryset:
            valida = False
            for horario in agenda.horarios.all():
                if agenda.dia == date.today() and horario.horario < datetime.now().time():
                    continue
                if (
                    Consulta.objects.filter(agenda__dia=agenda.dia, horario=horario.horario).count()
                    == 0
                ):
                    valida = True

            if not valida:
                agendas_invalidas.append(agenda.pk)

        if len(agendas_invalidas) > 0:
            for agenda in agendas_invalidas:
                # remove as agenda que já tem todos os seus horarios ocupados da listagem
                queryset = queryset.exclude(pk=agenda)

        return queryset


class ConsultaAPIView(generics.ListCreateAPIView):
    write_serializer_class = ConsultaWriteSerializer
    read_serializer_class = ConsultaReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Consulta.objects.filter(
            Q(usuario=self.request.user) & Q(agenda__dia__gte=date.today())
            | (Q(agenda__dia=date.today()) & Q(horario__gte=datetime.now().time()))
        )


class ConsultaDeleteApiView(RetrieveDestroyAPIView):

    serializer_class = ConsultaReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Consulta.objects.filter(usuario=self.request.user).filter(
            Q(agenda__dia__gt=date.today())
            | (Q(agenda__dia=date.today()) & Q(horario__gte=datetime.now().time()))
        )
