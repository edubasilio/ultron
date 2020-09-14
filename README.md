# Ultron
Pequena API REST para pesquisa na base de dados Ultron

# Arquitetura
![Alt text](project/ultron-arch-diagram.png?raw=true "Arquiteruta Ultron")

# Tecnologias
* **Python** como linhguagem de programação
* **Django** como framework de aplicação web
* **Django Rest Framework** como lib de aplicações REST
* **Docker** como gerenciador de container
* **Docker Composer** como orquestrador de container
* **Gunicorn** como servidor de produção
* **Nginx** como servidor proxy
* **Postgres** como _engine_ de banco de dados

# Instalação
1. Na máquina _host_, [instale o Docker e Docker-Compose](https://medium.com/@basiliocode/install-docker-on-ubuntu-18-04-71d91c3911c5);
2. Faça o download deste repositório git;
3. No diretório `raiz` (diretório que contém o arquivo `docker-compose.yml`), crie um arquivo `.env` para guardar as variáveis de ambiente do projeto. Segue um exemplo do arquivo `.env`:
```env
MULTISTAGE=LOCAL
SECRET_KEY=+p1-v2)-1mgln%m2&_3bxkszjx^89g3jbonf(kz1o605n=b7-&

DB_DATA_PATH=/caminho/absoluto/para/data
DB_ENGINE=django.db.backends.postgresql
DB_NAME=ultron
DB_USER=ultron_user
DB_PASSWORD=password
DB_HOST=database/url
DB_PORT=5432

ALLOWED_HOSTS=.ultron.com
HOST_HTTP_PORT=80
HOST_HTTP_DEV_PORT=8000
GUNICORN_WORKERS=2

KIBANA_PORT=5601
ELASTICSEARCH_PORT=9200
ELASTICSEARCH_DATA_PATH=/home/basilio/Sistemas/Ultron/elasticsearch_data
```

Para um teste rápido deste projeto, utilize os valores já setados acima modificando apenas: `ALLOWED_HOSTS`, `HOST_HTTP_PORT` e `HOST_HTTP_DEV_PORT`.

Sobre as variáveis de ambiente:
* `MULTISTAGE` Define o [stage](https://medium.com/@basiliocode/desenvolvimento-de-software-com-multi-stage-8caa38ca7a46) da aplicação. Quando setado para `PROD` o django executará com [settings.DEBUG](https://docs.djangoproject.com/en/3.0/ref/settings/#debug) = `False` no servidor de produção GUNICORN. Caso o valor seja diferente de `PROD`, `settings.DEBUG` receberá `True` e, além do servidor GUNICORN, o servidor de desenvolvimento do django, o _runserver_, será iniciado na porta definida em `HOST_HTTP_DEV_PORT`
* `SECRET_KEY` Define a [chave de segurança](https://docs.djangoproject.com/en/3.0/ref/settings/#secret-key) do projeto django
* `STATICFILES_PATH` Caminho absoluto do diretório em que será arquivado os arquivos estáticos do projeto (html, css, js, etc). Em sua máquina host, crie este diretório (fora do diretório versionado) e registre o caminho absoluto aqui
* `STATIC_URL` [Define a URL de acesso aos arquivos estáticos.](https://docs.djangoproject.com/en/3.0/ref/settings/#static-url) **Deve finalizar com /**
* `MEDIA_PATH` Caminho absoluto do diretório em que será arquivado os arquivos enviados pelo usuário. Em sua máquina host, crie este diretório (fora do diretório versionado) e registre o caminho absoluto aqui
* `MEDIA_URL` [Define a URL de acesso aos arquivos medias](https://docs.djangoproject.com/en/3.0/ref/settings/#media-url). **Deve finalizar com /**
* `DB_DATA_PATH` Caminho absoluto do diretório em que será arquivado os dados do banco de dados. Em sua máquina host, crie este diretório (fora do diretório versionado) e registre o caminho absoluto aqui
* `DB_ENGINE` Define a engine do banco de dados utilizado pelo projeto. O banco de dados deste projeto é o PostgreSQL, portanto, a engine deve ser: `django.db.backends.postgresql`. Mais informações na [documentação](https://docs.djangoproject.com/en/3.0/ref/settings/#engine) do django
* `DB_NAME` Define o nome do schema no banco de dados a ser utilizado pelo projeto
* `DB_USER` Define o nome de usuário a ser usado para acessar o banco de dados
* `DB_PASSWORD` Define o password do usuário do banco de dados
* `DB_HOST` [Define o endereço do banco de dados](https://docs.djangoproject.com/en/3.0/ref/settings/#host). Neste projeto, o endereço do container docker com o banco de dados é `db`
* `DB_PORT` Define a porta de acesso do banco de dados. O banco de dados no container docker deste projeto escuta a porta 5432
* `ALLOWED_HOSTS` Define as [URLs válidas](https://docs.djangoproject.com/en/3.0/ref/settings/#allowed-hosts) de acesso ao sistema separadas por espaço. Para acessar o sistema localmente, edite o arquivo `hosts` (`/etc/hosts no Ubuntu`) na máquina host recionando a URL para a máquina local
* `HOST_HTTP_PORT` Define a porta, na máquina host, de acesso HTTP ao sistema. **Certifique-se de que esta porta na máquina host esteja livre**. No Docker a requisição passará pelo servidor proxy (NGINX) no container docker `ultron_proxy` que redirecionará para o servidor da aplicação (GUNICORN) no container docker `ultron_web`
* `HOST_HTTP_DEV_PORT` Define a porta, na máquina host, de acesso direto ao sistema através do servidor de desenvolvimento _runserver_ do django. **Certifique-se de que esta porta na máquina host esteja livre**. Este servidor só funcionará quando o valor de `MULTISTAGE` for diferente de `PROD`
* `GUNICORN_WORKERS` Define a [quantidade de workers](https://docs.gunicorn.org/en/stable/configure.html#configuration-file) para o servidor de produção Gunicorn
* `KIBANA_PORT=5601`
* `ELASTICSEARCH_PORT`
* `ELASTICSEARCH_DATA_PATH` Certifique-se de que o container docker tenha permissão de escrita neste diretório. Para efeito de teste, recomenda-se usar permissão 777

# Rodando

## Iniciar o serviço
Com o terminal no diretório `ultron` (diretório que contém o arquivo `docker-compose.yml`), faça:
```sh
docker-compose up -d --build
```

## Parar o serviço
```sh
docker-compose down
```

## Criar um superusuário no sistema _ultron-web_
Com o serviço iniciado, no terminal faça:
```sh
docker exec -it ultron_web poetry run ./manage.py createsuperuser
```

# Para o Desenvolvedor
## Diagrama de Classes

![Alt text](project/ultron-class-diagram.png?raw=true "Diagrama de Classes")

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)