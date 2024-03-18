# Teste Técnico (Data Engineer)

Proposta de solução para o [desafio de data engineering](https://github.com/caiuafranca/test_data_engineer).

## O que fazer no desafio técnico?

- Ambiente em docker (MySQL, Airflow, Amundsen)
- Dag para extrair os metadados do MySQL e salvar no Amundsen
- Dag para extrair os metadados do Postgres e salvar no Amundsen

## Arquitetura da solução

```mermaid
    flowchart TD
        subgraph DAG_MYSQL[Metadados MySQL DAG]
            extracao_mysql_task --> indexacao_metadados_mysql_task
        end

        subgraph DAG_POSTGRES[Metadados Postgres DAG]
            extracao_postgres_task --> indexacao_metadados_postgres_task
        end

        subgraph PLUGIN[Plugin]
            extracao_mysql_task --> extracao_mysql
            extracao_postgres_task --> extracao_postgres
            indexacao_metadados_mysql_task --> indexacao_metadados
            indexacao_metadados_postgres_task --> indexacao_metadados
        end
```