from django_filters import rest_framework as filters
from .models import Medico, Especialidade


class MedicoFilter(filters.FilterSet):
    search = filters.CharFilter(field_name="nome", lookup_expr="istartswith")
    especialidade = filters.ModelMultipleChoiceFilter(
        field_name="especialidade", queryset=Especialidade.objects.all()
    )

    class Meta:
        model = Medico
        fields = ["search", "especialidade"]
