from datetime import date
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from .validations import no_past


class Especialidade(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Medico(models.Model):
    nome = models.CharField(max_length=100)
    crm = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=15, blank=True)
    especialidade = models.ForeignKey(Especialidade,
                                      on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Agenda(models.Model):
    medico = models.ForeignKey(Medico,
                               unique_for_date="dia",
                               on_delete=models.CASCADE)
    dia = models.DateField(validators=[no_past])
    horarios = ArrayField(models.TimeField())

    def __str__(self):
        return f'{self.medico.nome} - {self.dia.strftime("%d/%m/%Y")}'

    class Meta:
        ordering = ['dia']


class Consulta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    dia = models.DateField()
    data_agendamento = models.DateTimeField(auto_now_add=True)
    horario = models.TimeField()
