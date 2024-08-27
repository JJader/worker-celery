# worker-celery

# Escopo

Worker para suportar os modelos de ML

# Como executar ?

- rodar o comando `docker-compose up --builder`

- Utilizar a api front-end [api-frontend](https://github.com/JJader/api-frontend/)

# Informações 

* O Worker as seguintes tasks:
    * `app.mlflow.tasks.load`
        * Faz o push do modelo no mlflow

    * `app.mlflow.tasks.predict`
        * Faz o pull do modelo e realiza a predição

# Todo

[x] caso der erro trazer o erro no get.load

[x] Arquitetura

[x] Exploração de dados

[x] add rota health

[x] add docker para api

[x] retornar informações do modelo

[x] histórico apenas do predict 

[x] testar modelo 

[x] reame.md fast api

[x] reame.md celery

[x] teste unitario api

[x] teste unitario worker

[] docstring



