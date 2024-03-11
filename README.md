# Teste Técnico

## Infra necessaria:

- Banco mysql - Backoffice
    - pasta Bancos tem uma estrutura em Docker
    - docker compose up
    - criar o banco com script dentro de banco/db

- Banco postgresql - ao subir o airflow no docker ele sobe um banco postgres

- Airflow
    - Seguir a documentação
    - docker compose up airflow-init
    - docker compose up

- Amundsen (amundsen_catalogo)
     -  docker-compose up dentro da pasta do amundsen

dentro das pastas tem o dockerfile e docker-compose das aplicações

## O que fazer neste desafio tecnico?

- 1 - subir o ambiente em docker

- 2 - Construir Dags em Python 
- 2.1 - Dag para extrair os metadados do mysql e salvar no amundsen
- 2.2 - Dag para extrair os metadados do postgres e salvar no amundsen

- 3 (opcional) - Subir um banco NoSQL nessa Infra e efetuar a extração dos metadados
-- OBS. a tecnologia(mongo, redis...) e os collection e documentos(banco,tabelas) ficam a seu criterio

# Entregavél para a validação

- A resolução em um repositorio no github
- Alem de subir o ambinente em Docker
- Ver os metadados na plataforma do amundsen - localhost:5000
- Par-programing com explanação do seu código

referencias:

- https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html
- https://github.com/amundsen-io/amundsen

