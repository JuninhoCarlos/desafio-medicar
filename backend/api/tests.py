from datetime import date
from datetime import datetime as dt
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from .models import Agenda, Especialidade, Horario, Medico


class APITest(APITestCase):
    def setUp(self):
        self.usuario = get_user_model().objects.create_user(username="api", password="secret")

        token = Token.objects.create(user=self.usuario)
        print("token:", token.key)
        self.cliente = APIClient()
        self.cliente.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        # Cadastro de especialidades
        pediatra = Especialidade.objects.create(nome="Pediatra")
        psicologo = Especialidade.objects.create(nome="Psicologo")
        ortopedista = Especialidade.objects.create(nome="Orpedista")
        otorrino = Especialidade.objects.create(nome="Otorrino")

        # Cadastro dos médicos
        juliette = Medico.objects.create(nome="Juliette", crm=5214, especialidade=pediatra)
        vihtube = Medico.objects.create(nome="Vihtube", crm=5472, especialidade=otorrino)
        # joao = Medico.objects.create(nome="Joao", crm=1334, especialidade=ortopedista)
        # camilla = Medico.objects.create(nome="lula", crm=1587, especialidade=psicologo)

        # Cadastrar alguns horários
        agora = dt.now()

        uma_hora = timedelta(hours=1)

        futuro = agora + uma_hora
        hora_futuro1 = Horario.objects.create(horario=futuro.time())

        futuro = futuro + uma_hora
        hora_futuro2 = Horario.objects.create(horario=futuro.time())

        # futuro = futuro + uma_hora
        # hora_futuro3 = Horario.objects.create(horario=futuro.time())

        passado = agora - uma_hora
        hora_passado = Horario.objects.create(horario=passado.time())

        # Cadastrar agendas
        # Agenda para hoje da Juliette
        agenda1 = Agenda(medico=juliette, dia=dt.today())
        agenda1.save()
        # Adiciona horarios validos à agenda
        agenda1.horarios.add(hora_futuro1, hora_futuro2)
        # Adiciona horarios invalidos (Dia de hoje, mas que já passou)
        agenda1.horarios.add(hora_passado)

        # Agenda para amanhã
        agenda2 = Agenda(medico=vihtube, dia=date.today() + timedelta(days=1))
        agenda2.save()
        # Adiciona horários e todos são válido, pois a agenda é para amanhã
        agenda2.horarios.add(hora_futuro1, hora_futuro2, hora_passado)

    def test_get_especialidades(self):
        url = reverse("get_especialidades")
        resposta = self.cliente.get(url, format="json")
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta.data), 4)
