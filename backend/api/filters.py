from django_filters import rest_framework as filters
from django_filters.widgets import RangeWidget, SuffixedMultiWidget

from .models import Agenda, Especialidade, Medico


class MedicoFilter(filters.FilterSet):
    search = filters.CharFilter(field_name="nome", lookup_expr="istartswith")
    especialidade = filters.ModelMultipleChoiceFilter(
        field_name="especialidade", queryset=Especialidade.objects.all()
    )

    class Meta:
        model = Medico
        fields = ["search", "especialidade"]


class MudaSufixoWidget(RangeWidget, SuffixedMultiWidget):
    suffixes = ["inicio", "final"]

    def __init__(self, attrs=None):
        super().__init__(attrs)


class AgendaFilter(filters.FilterSet):
    medico = filters.ModelMultipleChoiceFilter(field_name="medico", queryset=Medico.objects.all())
    especialidade = filters.ModelMultipleChoiceFilter(
        field_name="medico__especialidade", queryset=Especialidade.objects.all()
    )
    data = filters.DateFromToRangeFilter(field_name="dia", widget=MudaSufixoWidget)
    # data_inicio = filters.DateFilter(
    #    field_name="dia",
    #    lookup_expr=("gte"),
    # )
    # data_fim = filters.DateFilter(field_name="dia", lookup_expr=("lte"))

    class Meta:
        model = Agenda
        fields = ["medico", "especialidade", "dia"]
