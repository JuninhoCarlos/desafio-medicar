# desafio-medicar

Um sistema intuito de auxiliar seus clientes na marcação de consultas e gerenciar seu corpo médico. Esse projeto foi desenvolvido como parte da avaliação do processo seletivo da IntMed-Software.

## Configuração

### Docker:

Caso não tenha o Docker e o Docker-compose, instale. Instruções de instalação pode ser encontradas em https://www.docker.com/get-started .

#### Passo 1

Crie um arquivo .env no diretório raiz do repositório para armazenar as variáveis de ambiente que o settings.py lê. Para simplicar essa configuração, o arquivo env.sample
já possui uma configuração válida para os containers docker que serão criados. Então, copie o conteúdo do env.sample para o arquivo .env.

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

- /api/v1/especialidades/ (get)
- /api/v1/medicos/ (get)
- /api/v1/agendas/ (get, post)
- /api/v1/consultas/ ( get,post,delete)

### O endpoint /api/v1/especialidades/

Lista todas as especialidades médicas disponíveis na clínica:

#### Requisição

```
GET /api/v1/especialidades/
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
GET /api/v1/especialidades/?search=ped
```

#### Resposta
