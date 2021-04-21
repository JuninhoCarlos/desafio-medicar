from django.core.exceptions import ValidationError
from django_filters import fields
from django_filters import rest_framework as filters
from django_filters.widgets import RangeWidget, SuffixedMultiWidget

from .models import Agenda, Especialidade, Medico


class CampoMultiEscolha(fields.ModelMultipleChoiceField):
    def _check_values(self, value):
        """
        Sobrescreve a classe base para que seja possivel filtar por pk
        que não exista, pois o comportamento padrão é retornar um
        bad request (400) enquanto o esperado é retornar um array vazio
        no caso de um filtro por uma chave inexistente
        """

        null = self.null_label is not None and value and self.null_value in value
        if null:
            value = [v for v in value if v != self.null_value]
        field_name = self.to_field_name or "pk"
        result = list(self.queryset.filter(**{"{}__in".format(field_name): value}))
        result += [self.null_value] if null else []
        return result

    def clean(self, value):

        value = self.prepare_value(value)

        # Caso onde não passou nenhum valor para a filtragem
        if not value:
            return self.queryset.all()

        if self.required and not value:
            raise ValidationError(self.error_messages["required"], code="required")
        elif not self.required and not value:
            return self.queryset.none()
        if not isinstance(value, (list, tuple)):
            raise ValidationError(
                self.error_messages["invalid_list"],
                code="invalid_list",
            )

        qs = self._check_values(value)
        # Since this overrides the inherited ModelChoiceField.clean
        # we run custom validators here
        self.run_validators(value)
        return qs


class FiltroMultiplaEscolha(filters.ModelMultipleChoiceFilter):
    """
    escreve um filtro customizado para o ModelMultipleChoiceFilter
    """

    field_class = CampoMultiEscolha

    def filter(self, qs, value):
        if len(value) > 0:
            return super().filter(qs, value)

        return qs.none()


class MedicoFilter(filters.FilterSet):
    search = filters.CharFilter(field_name="nome", lookup_expr="istartswith")
    especialidade = FiltroMultiplaEscolha(
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
    medico = FiltroMultiplaEscolha(field_name="medico", queryset=Medico.objects.all())
    especialidade = FiltroMultiplaEscolha(
        field_name="medico__especialidade", queryset=Especialidade.objects.all()
    )
    data = filters.DateFromToRangeFilter(field_name="dia", widget=MudaSufixoWidget)

    class Meta:
        model = Agenda
        fields = ["medico", "especialidade", "dia"]
