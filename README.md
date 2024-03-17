# Teste Técnico

## O que fazer neste desafio tecnico?

- [OK] Ambiente em docker
- [OK] Dag para extrair os metadados do mysql e salvar no amundsen
- [OK] Dag para extrair os metadados do postgres e salvar no amundsen
- [NOK] (opcional) Subir um banco NoSQL e efetuar a extração dos metadados

## Arquitetura da solução

```mermaid
    flowchart TD
        subgraph DAG_MYSQL[Metadados MySQL DAG]
            extracao_mysql_task --> indexacao_metadados_mysql_task
        end

        subgraph DAG_POSTGRES[Metadados Postgres DAG]
            extracao_postgres_task --> indexacao_metadados_postgres_task
        end

        subgraph PLUGGIN
            extracao_mysql_task --> extracao_mysql
            extracao_postgres_task --> extracao_postgres
            indexacao_metadados_mysql_task --> indexacao_metadados
            indexacao_metadados_postgres_task --> indexacao_metadados
        end
```