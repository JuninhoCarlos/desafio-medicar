from django.db import models
from django.core.exceptions import ValidationError
from datetime import date


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


class Horario(models.Model):
    horario = models.TimeField(unique=True)

    def __str__(self):
        return str(self.horario.strftime("%H:%M:%S"))


class Agenda(models.Model):
    medico = models.ForeignKey(Medico,
                               unique_for_date="dia",
                               on_delete=models.CASCADE)
    dia = models.DateField()
    horarios = models.ManyToManyField(Horario)

    def __str__(self):
        return self.medico.nome + " - " + str(self.dia.strftime("%d/%m/%Y"))

    def clean(self):
        if self.dia < date.today():
            raise ValidationError('The agenda should be contain a valid'
                                  ' date (from today onwards)')
