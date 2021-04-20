# desafio-medicar

Um sistema intuito de auxiliar seus clientes na marcação de consultas e gerenciar seu corpo médico. Esse projeto foi desenvolvido como parte da avaliação do processo seletivo da IntMed-Software.

## Configuração

### Docker:

Caso não tenha o Docker e o Docker-compose, instale. Instruções de instalação pode ser encontradas em https://www.docker.com/get-started .

#### Passo 1

Clone o repositorio no diretório de sua preferência e acesse o diretório

```
$ git clone https://github.com/JuninhoCarlos/desafio-medicar.git
$ cd desafio-medicar
```

#### Passo 2

Crie a imagem e ative os dois containers (servidor web(web) e banco de dados(db))

```
$ sudo docker-compose up -d --build
```

Ao finalizar esse passo você já deve ter os dois containers executando

#### Passo 3

Crie o banco de dados da aplicação executando um migrate

```
$ sudo docker-compose exec web python manage.py migrate
```

#### Passo 4

Crie um usuário para o django-admin

```
$ sudo docker-compose exec web python manage.py createsuperuser
```

e informe os dados do usuário. Depois de finalizado esse passo você está apto a
acessar a página de admin do sistema em http://localhost:8000/admin/ informando as
credencias que você acabou de criar.

Ao final desses passos você terá dois containers Docker executando:

- **servidor web: **porta 8000
- **servidor do banco de dados: **5432

Caso você deseje encerrar esse containers para, digite o comando:

```
$ docker-compose down
```

## Executando Testes

Para executar os testes unitários da API execute:

```
$ sudo docker-compose exec web python manage.py test
```
