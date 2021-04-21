# desafio-medicar

Um sistema intuito de auxiliar seus clientes na marcação de consultas e gerenciar seu corpo médico. Esse projeto foi desenvolvido como parte da avaliação do processo seletivo da IntMed-Software.

## Configuração

### Docker:

Caso não tenha o Docker e o Docker-compose, instale. Instruções de instalação pode ser encontradas em https://www.docker.com/get-started .

#### Passo 1

Crie um arquivo .env no diretório raiz do repositório para armazenar as variáveis de ambiente que o settings.py lê. Para simplicar essa configuração, o arquivo env.sample
já possui uma configuração válida para os containers docker que serão criados. Então, copie o conteúdo do env.sample para o arquivo .env. Isso pode ser feito com o comando:

```
$ cat env.sample > .env
```

#### Passo 2

Depois de instalado o Docker, clone o repositorio no diretório de sua preferência e acesse o diretório

```
$ git clone https://github.com/JuninhoCarlos/desafio-medicar.git
$ cd desafio-medicar
```

#### Passo 3

Crie a imagem e ative os dois containers (servidor web(web) e banco de dados(db))

```
$ sudo docker-compose up -d --build
```

Ao finalizar esse passo você já deve ter os dois containers executando

#### Passo 4

Crie o banco de dados da aplicação executando um migrate

```
$ sudo docker-compose exec web python manage.py migrate
```

#### Passo 5

Crie um usuário para o django-admin

```
$ sudo docker-compose exec web python manage.py createsuperuser
```

e informe os dados do usuário. Depois de finalizado esse passo você está apto a
acessar a página de admin do sistema em http://localhost:8000/admin/ informando as
credencias que você acabou de criar.

Ao final desses passos você terá dois containers Docker executando:

- servidor web: porta 8000
- servidor do banco de dados: 5432

Caso você deseje encerrar esses containers, digite o comando:

```
$ docker-compose down
```

## Executando Testes

Para executar os testes unitários da API execute:

```
$ sudo docker-compose exec web python manage.py test
```

# Funcionalidades da Interface Administrativa

A interface administrativa (http://localhost:8000/admin/) possui as seguintes funcionalidades:

## Cadastrar especialidade

É possivel cadastrar as especialidades médicas (ex: Cardiologia, Pediatria) que a clínica atende fornecendo as seguintes entradas:

- Nome: Nome da especialidade (obrigatório)

## Cadastrar médicos

É possível cadastrar os médicos que podem atender na clínica fornecendo as seguintes informações:

- Nome: Nome do médico (obrigatório)
- CRM: Número do médico no conselho regional de medicina (obrigatório)
- E-mail: Endereço de e-mail do médico
- Telefone: Telefone do médico
- Especialidade: Especialidade na qual o médico atende

## Criar agenda para médico

Deve ser possível criar uma agenda para um médico em um dia específico fornecendo as seguintes informações:

- Médico: Médico que será alocado (obrigatório)
- Dia: Data de alocação do médico (obrigatório)
- Horários: Lista de horários na qual o médico deverá ser alocado para o dia especificado (obrigatório)

# Recursos da API

A API utiliza autenticação baseada em token, então, ao enviar a requisição, o cliente deve enviar no cabeçalho HTTP Authorization o token de autenticação.
Todos os endpoints exigem autenticação.

Para uma descrição detalhada das regras de negócios e todas as funcionalidades, você pode consultar o repositório do
desafio https://github.com/Intmed-Software/desafio/tree/master/backend.

## Endpoints disponíveis:

Os endpoints disponíveis e os métodos HTTP permitidos são:

- /login/ (post)
- /especialidades/ (get)
- /medicos/ (get)
- /agendas/ (get)
- /consultas/ (get,post,delete)

### O endpoint /login/
Autentica o usuário e retorna o token de acesso à API

#### Requisição

Manda as credenciais e recebe o token como retorno

```
POST /auth/login/
{
  "username": "admin",
  "password": "admin"
}
```

#### Resposta
```json
  {
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",    
  }
```


### O endpoint /especialidades/

Lista todas as especialidades médicas disponíveis na clínica:

#### Requisição

```
GET /especialidades/
```

#### Resposta

```json
[
  {
    "id": 1,
    "nome": "Pediatria"
  },
  {
    "id": 2,
    "nome": "Ginecologia"
  },
  {
    "id": 3,
    "nome": "Cardiologia"
  },
  {
    "id": 4,
    "nome": "Clínico Geral"
  }
]
```

#### Filtros

- Nome da especialidade (termo de pesquisa)

```
GET /especialidades/?search=ped
```

### O endpoint /medicos/

Lista todos os médicos que atendem pela clínica

#### Requisição

```
GET /medicos/
```

#### Resposta

```json
[
  {
    "id": 1,
    "crm": 3711,
    "nome": "Drauzio Varella",
    "especialidade": {
      "id": 2,
      "nome": "Pediatria"
    }
  },
  {
    "id": 2,
    "crm": 2544,
    "nome": "Gregory House",
    "especialidade": {
      "id": 3,
      "nome": "Cardiologia"
    }
  },
  {
    "id": 3,
    "crm": 3087,
    "nome": "Tony Tony Chopper",
    "especialidade": {
      "id": 2,
      "nome": "Pediatria"
    }
  }
]
```

#### Filtros

- Identificador de uma ou mais especialidades
- Nome do médico (termo de pesquisa)

```
GET /medicos/?search=maria&especialidade=1&especialidade=3
```

### O endpoint /consultas/

#### Listar consultas marcadas

Lista todas as consultas marcadas do usuário logado

##### Requisição

```
GET /consultas/
```

##### Retorno

```json
[
  {
    "id": 1,
    "dia": "2020-02-05",
    "horario": "12:00",
    "data_agendamento": "2020-02-01T10:45:0-03:00",
    "medico": {
      "id": 2,
      "crm": 2544,
      "nome": "Gregory House",
      "especialidade": {
        "id": 3,
        "nome": "Cardiologia"
      }
    }
  },
  {
    "id": 2,
    "dia": "2020-03-01",
    "horario": "09:00",
    "data_agendamento": "2020-02-01T10:45:0-03:00",
    "medico": {
      "id": 1,
      "crm": 3711,
      "nome": "Drauzio Varella",
      "especialidade": {
        "id": 2,
        "nome": "Pediatria"
      }
    }
  }
]
```

#### Marcar consulta

Marca uma consulta para o usuário logado

##### Requisição

```
POST /consultas/
{
  "agenda_id": 1,
  "horario": "14:15"
}
```

##### Retorno

```json
{
  "id": 2,
  "dia": "2020-03-01",
  "horario": "09:00",
  "data_agendamento": "2020-02-01T10:45:0-03:00",
  "medico": {
    "id": 1,
    "crm": 3711,
    "nome": "Drauzio Varella",
    "especialidade": {
      "id": 2,
      "nome": "Pediatria"
    }
  }
}
```

#### Desmarcar consulta

Desmarca uma consulta marcada pelo usuário

##### Requisição

```
DELETE /consultas/<consulta_id>
```

##### Retorno

Não há retorno (vazio)

### O endpoint /agendas/

Lista todas as agendas disponíveis na clínica

#### Requisição

```
GET /agendas/
```

#### Retorno

```json
[
  {
    "id": 1,
    "medico": {
      "id": 3,
      "crm": 3087,
      "nome": "Tony Tony Chopper",
      "especialidade": {
        "id": 2,
        "nome": "Pediatria"
      }
    },
    "dia": "2020-02-10",
    "horarios": ["14:00", "14:15", "16:00"]
  },
  {
    "id": 2,
    "medico": {
      "id": 2,
      "crm": 2544,
      "nome": "Gregory House",
      "especialidade": {
        "id": 3,
        "nome": "Cardiologia"
      }
    },
    "dia": "2020-02-10",
    "horarios": ["08:00", "08:30", "09:00", "09:30", "14:00"]
  }
]
```

#### Filtros

- Identificador de um ou mais médicos
- Identificador de uma ou mais especialidades
- Intervalo de data

```
GET /agendas/?medico=1&especialidade=2&data_inicio=2020-01-01&data_final=2020-01-05
```
