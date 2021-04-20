from datetime import datetime as dt
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from .models import Agenda, Consulta, Especialidade, Horario, Medico


def dump():

    for agenda in Agenda.objects.all():
        print("agenda:", agenda)
        for horario in agenda.horarios.all():
            print("horario:", horario.horario)
        print()


class APITest(APITestCase):
    def setUp(self):
        """
        Configura o ambiente de teste
        """

        # Cria dois usuários diferentes para o teste
        # usuario api
        self.usuario_api = get_user_model().objects.create_user(username="api", password="secret")
        token = Token.objects.create(user=self.usuario_api)
        self.cliente_api = APIClient()
        self.cliente_api.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        # usuario teste
        self.usuario_teste = get_user_model().objects.create_user(
            username="teste", password="secret"
        )
        token_teste = Token.objects.create(user=self.usuario_teste)
        self.cliente_teste = APIClient()
        self.cliente_teste.credentials(HTTP_AUTHORIZATION="Token " + token_teste.key)

        # Cadastro de especialidades
        self.pediatra = Especialidade.objects.create(nome="Pediatra")
        self.ortopedista = Especialidade.objects.create(nome="Orpedista")
        self.otorrino = Especialidade.objects.create(nome="Otorrino")

        # Cadastro dos médicos
        self.medica_juliette = Medico.objects.create(
            nome="Juliette", crm=5214, especialidade=self.pediatra
        )
        self.medica_vihtube = Medico.objects.create(
            nome="Vihtube", crm=5472, especialidade=self.otorrino
        )
        self.medico_joao = Medico.objects.create(
            nome="Joao", crm=1334, especialidade=self.ortopedista
        )
        self.medica_camilla = Medico.objects.create(
            nome="Camilla", crm=1587, especialidade=self.pediatra
        )

        # Cadastrar alguns horários
        agora = dt.now()

        futuro_1 = agora + timedelta(minutes=5)
        hora_futuro1 = Horario.objects.create(horario=futuro_1.time())

        futuro_2 = futuro_1 + timedelta(minutes=5)
        self.hora_futuro2 = Horario.objects.create(horario=futuro_2.time())

        hora_generica = Horario.objects.create(horario="14:00")
        hora_generica_2 = Horario.objects.create(horario="15:00")

        passado = agora - timedelta(minutes=5)
        hora_passado = Horario.objects.create(horario=passado.time())

        # Cadastrar agendas
        # Agenda para hoje da Juliette
        self.hoje = dt.today()
        self.agenda_hoje = Agenda(medico=self.medica_juliette, dia=self.hoje)
        self.agenda_hoje.save()
        # Adiciona horarios validos à agenda
        self.agenda_hoje.horarios.add(hora_futuro1, self.hora_futuro2)
        # Adiciona horarios invalidos (Dia de hoje, mas que já passou)
        self.agenda_hoje.horarios.add(hora_passado)

        # Agenda para amanhã
        self.amanha = self.hoje + timedelta(days=1)
        self.agenda_amanha = Agenda(medico=self.medica_vihtube, dia=self.amanha)
        self.agenda_amanha.save()
        # Adiciona horários e todos são válido, pois a agenda é para amanhã
        self.agenda_amanha.horarios.add(
            hora_futuro1, self.hora_futuro2, hora_passado, hora_generica, hora_generica_2
        )

        # Agenda passada
        self.agenda_ontem = Agenda(medico=self.medico_joao, dia=self.hoje - timedelta(days=1))
        self.agenda_ontem.save()
        self.agenda_ontem.horarios.add(hora_futuro1, self.hora_futuro2, hora_passado, hora_generica)

        url_consultas = reverse("consultas_post")

        # Cadastra algumas consultas para hoje e amanhã
        res = self.cliente_api.post(
            url_consultas, {"agenda_id": self.agenda_hoje.pk, "horario": futuro_1.time()}
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.pk_consulta = res.data["id"]

        self.consulta_passada = Consulta.objects.create(
            horario="14:00",
            usuario=self.usuario_api,
            agenda=self.agenda_ontem,
        )

        self.cliente_api.post(
            url_consultas, {"agenda_id": self.agenda_amanha.pk, "horario": passado.time()}
        )
        self.cliente_api.post(
            url_consultas, {"agenda_id": self.agenda_amanha.pk, "horario": futuro_1.time()}
        )
        self.cliente_api.post(
            url_consultas, {"agenda_id": self.agenda_amanha.pk, "horario": futuro_2.time()}
        )

    def teste_get_especialidades(self):
        """
        Testa o GET request no endpoint especialidades
        que deve retornar todas as especialidades cadastradas no banco
        """
        url = reverse("get_especialidades")
        resposta = self.cliente_api.get(url, format="json")
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta.data), 3)

    def teste_busca_especialidades(self):
        """
        Testa a pesquisa em especialidades (?search=)
        """
        url = reverse("get_especialidades") + "?search=ped"
        resposta = self.cliente_api.get(url, format="json")
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta.data), 1)

        url = reverse("get_especialidades") + "?search=o"
        resposta = self.cliente_api.get(url, format="json")
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta.data), 2)

    def teste_get_medicos(self):
        """
        Testa o GET request no endpoint medicos
        que deve retornar todos os médicos cadastrados no banco
        """
        url = reverse("get_medicos")
        resposta = self.cliente_api.get(url)
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta.data), 4)

    def teste_busca_medicos(self):
        """
        Testa a busca (?search) pelo nome do médico
        """
        url = reverse("get_medicos") + "?search=ju"
        resposta = self.cliente_api.get(url)
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(resposta.data[0]["nome"], "Juliette")

        url = reverse("get_medicos") + "?search=j"
        resposta = self.cliente_api.get(url)
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta.data), 2)

    def teste_filtro_medicos(self):
        """
        Testa o filtro de especialidade
        """
        url = f'{reverse("get_medicos")}?especialidade={self.ortopedista.pk}'
        resposta = self.cliente_api.get(url)
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(resposta.data[0]["nome"], "Joao")

        url = (
            f'{reverse("get_medicos")}?especialidade={self.ortopedista.pk}'
            f"&especialidade={self.pediatra.pk}"
        )
        resposta = self.cliente_api.get(url)
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta.data), 3)

    def teste_filtro_busca_medicos(self):
        """
        Testa a busca e o filtro juntos
        (atualmente funciona como um or (search | especialidae))
        """
        url = f'{reverse("get_medicos")}?search=jo?especialidade={self.ortopedista.pk}'
        resposta = self.cliente_api.get(url)
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(resposta.data[0]["nome"], "Joao")

        url = (
            f'{reverse("get_medicos")}?search=J?especialidade={self.ortopedista.pk}'
            f"&especialidade={self.pediatra.pk}"
        )
        resposta = self.cliente_api.get(url)
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta.data), 2)

    def teste_get_agenda_disponiveis(self):
        """
        Testa se lista somente as agendas disponiveis e não mostra
        as agendas para datas passadas
        """
        url = reverse("get_agendas")
        resposta = self.cliente_api.get(url)
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta.data), 2)

    def teste_agenda_horario_excluido(self):
        """
        Testa se o horário é removido da listagem da agenda disponivel
        quando se marcar uma consulta para ele
        """
        url = reverse("get_agendas")
        resposta = self.cliente_api.get(url)
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta.data[1]["horarios"]), 2)

        url = reverse("consultas_post")
        resposta = self.cliente_api.post(
            url, {"agenda_id": self.agenda_amanha.pk, "horario": "14:00"}
        )
        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)

        # Depois da inserção deve ter só 1 horario disponivel agora
        url = reverse("get_agendas")
        resposta = self.cliente_api.get(url)
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta.data[1]["horarios"]), 1)

    def teste_filtro_medico_agenda(self):
        """
        Testa o filtro de medico aplicado no endpoint agenda
        """
        url = f'{reverse("get_agendas")}?medico={self.medico_joao.pk}'
        resposta = self.cliente_api.get(url)
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta.data), 0)

        url = f'{reverse("get_agendas")}?medico={self.medica_juliette.pk}'
        resposta = self.cliente_api.get(url)
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta.data), 1)

    def teste_filtro_especialidade_agenda(self):
        """
        Testa o filtro de especialidade aplicado no endpoint agenda
        """
        url = f'{reverse("get_agendas")}?especialidade={self.pediatra.pk}'
        resposta = self.cliente_api.get(url)
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta.data), 1)

    def teste_filtro_data_agenda(self):
        """
        Testa o filtro de especialidade aplicado no endpoint agenda
        """
        url = (
            f'{reverse("get_agendas")}?data_inicio={self.hoje.date()}&data_final={self.hoje.date()}'
        )
        resposta = self.cliente_api.get(url)
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta.data), 1)

    def teste_todos_filtros_agenda(self):
        """
        Testa a combinação dos filtros do endpoint agenda
        """
        url = (
            f'{reverse("get_agendas")}?medico={self.medica_juliette.pk}'
            f"&especialidade={self.pediatra.pk}&data_inicio={self.hoje.date()}"
            f"&data_final={self.hoje.date()}"
        )
        print(url)
        resposta = self.cliente_api.get(url)
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta.data), 1)

    def teste_horario_excluido_agenda(self):
        """
        Teste se os horarios passados sao removidos da listagem da agenda e se o
        horario marcado esta sendo removido da listagem
        """
        url = (
            f'{reverse("get_agendas")}?data_inicio={self.hoje.date()}&data_final={self.hoje.date()}'
        )
        resposta = self.cliente_api.get(url)

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta.data[0]["horarios"]), 1)

    def teste_agenda_excluida_quando_cheia(self):
        """
        Teste se a agenda desaparece da listagem quando tem todos os seus horarios
        preenchidos, pois não há mais horários disponíveis
        """
        url = (
            f'{reverse("get_agendas")}?data_inicio={self.hoje.date()}&data_final={self.hoje.date()}'
        )
        resposta = self.cliente_api.get(url)
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta.data[0]["horarios"]), 1)

        # Agenda consulta no último horario disponivel nessa agenda
        url = reverse("consultas_post")
        resposta = self.cliente_api.post(
            url, {"agenda_id": self.agenda_hoje.pk, "horario": self.hora_futuro2.horario}
        )
        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)

        # Deve retornar um array vazio
        url = (
            f'{reverse("get_agendas")}?data_inicio={self.hoje.date()}&data_final={self.hoje.date()}'
        )
        resposta = self.cliente_api.get(url)
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta.data), 0)

    def teste_get_consultas(self):
        """
        Testa se lista somente as consultas que não passaram o dia e o horario
        """
        url = reverse("consultas_post")
        resposta = self.cliente_api.get(url)
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta.data), 4)

    def teste_marcar_consulta(self):
        """
        Teste o caso onde a insercao da certo
        """
        url = reverse("consultas_post")
        resposta = self.cliente_api.post(
            url, {"agenda_id": self.agenda_amanha.pk, "horario": "14:00"}
        )
        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)

    def teste_marcar_consulta_dia_passado(self):
        """
        Testa a inserção em um dia passado
        """
        url = reverse("consultas_post")
        resposta = self.cliente_api.post(
            url, {"agenda_id": self.agenda_ontem.pk, "horario": "14:00"}
        )
        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)

    def teste_marcar_consulta_mesmo_horario(self):
        """
        Testa a inserção em um dia e horário que o usuário já tem outra
        consulta marcada no mesmo dia e horario
        """
        url = reverse("consultas_post")
        resposta = self.cliente_api.post(
            url, {"agenda_id": self.agenda_amanha.pk, "horario": "14:00"}
        )
        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)

        # marcando consulta para o mesmo dia e horarios para esse usuario
        url = reverse("consultas_post")
        resposta = self.cliente_api.post(
            url, {"agenda_id": self.agenda_amanha.pk, "horario": "14:00"}
        )
        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)

    def teste_marcar_consulta_horario_ocupado(self):
        """
        Testa a inserção em um dia e horário que já está ocupado por
        outro usuario
        """
        url = reverse("consultas_post")
        resposta = self.cliente_api.post(
            url, {"agenda_id": self.agenda_amanha.pk, "horario": "14:00"}
        )
        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)

        # usuario teste tenta marcar a consulta no mesmo dia e horario
        # do usuário api
        url = reverse("consultas_post")
        resposta = self.cliente_teste.post(
            url, {"agenda_id": self.agenda_amanha.pk, "horario": "14:00"}
        )
        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)

    def teste_desmarcar_consulta(self):
        """
        Testa o caso de sucesso da desmarcação de consulta
        """
        url = f'{reverse("consultas_post")}{self.pk_consulta}/'
        resposta = self.cliente_api.delete(url)
        self.assertEqual(resposta.status_code, status.HTTP_204_NO_CONTENT)

    def teste_desmacar_consulta_inexistente(self):
        """
        Testa caso onde tenta desmarcar uma consulta que não existe
        """
        url = f'{reverse("consultas_post")}546846/'
        resposta = self.cliente_api.delete(url)
        self.assertEqual(resposta.status_code, status.HTTP_404_NOT_FOUND)

    def teste_desmacar_consulta_do_outro(self):
        """
        Testa caso onde um usuario manda um delete para uma consulta
        que existe, mas não pertence a ele
        """
        url = f'{reverse("consultas_post")}{self.pk_consulta}/'
        resposta = self.cliente_teste.delete(url)
        self.assertEqual(resposta.status_code, status.HTTP_404_NOT_FOUND)

    def teste_desmarcar_consulta_passada(self):
        """
        Testa caso onde o usuario tenta desmarcar uma consulta
        que ja aconteceu
        """
        url = f'{reverse("consultas_post")}{self.consulta_passada.pk}/'
        resposta = self.cliente_teste.delete(url)
        self.assertEqual(resposta.status_code, status.HTTP_404_NOT_FOUND)
