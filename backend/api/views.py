from rest_framework import mixins, viewsets, filters

from .serializers import EspecialidadeSerializer
from .models import Especialidade


class EspecialidadeView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Especialidade.objects.all()
    serializer_class = EspecialidadeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^nome']
