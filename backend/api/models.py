from django.contrib.auth import get_user_model
from django.db import models

from .validations import no_past


class Especialidade(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Medico(models.Model):
    nome = models.CharField(max_length=100)
    crm = models.BigIntegerField()
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=15, blank=True)
    especialidade = models.ForeignKey(Especialidade, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Horario(models.Model):
    horario = models.TimeField(unique=True)

    def __str__(self):
        return self.horario.isoformat()

    class Meta:
        ordering = ["horario"]


class Agenda(models.Model):
    medico = models.ForeignKey(Medico, unique_for_date="dia", on_delete=models.CASCADE)
    dia = models.DateField(validators=[no_past])
    horarios = models.ManyToManyField(Horario)

    def __str__(self):
        return f'{self.medico.nome} - {self.dia.strftime("%d/%m/%Y")}'

    class Meta:
        ordering = ["dia"]


class Consulta(models.Model):
    usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    data_agendamento = models.DateTimeField(auto_now_add=True)
    horario = models.TimeField()
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)

    class Meta:
        ordering = ["agenda", "horario"]
