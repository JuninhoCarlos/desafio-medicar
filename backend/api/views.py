from django.db.models import Q
from rest_framework import mixins, viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .serializers import EspecialidadeSerializer, MedicoSerializer, AgendaSerializer
from .models import Especialidade, Medico, Agenda


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
        nomeFilter = self.request.query_params.get('search', None)
        especialidadesFilter = self.request.query_params.getlist('especialidade', None)

        if nomeFilter:
            queryset = queryset.filter(Q(nome__startswith=nomeFilter))
        if especialidadesFilter:
            query = Q()
            for especilidade in especialidadesFilter:
                query |= Q(especialidade=especilidade)
            queryset = queryset.filter(query)

        return queryset


class AgendaViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = AgendaSerializer
    permission_classes = [IsAuthenticated]
    queryset = Agenda.objects.all()