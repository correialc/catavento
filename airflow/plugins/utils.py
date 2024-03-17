from airflow.hooks.base_hook import BaseHook

def get_conexao_airflow(id_conexao: str) -> str:
    """Retorna uma conexao armazenada previamente no Airflow"""
    conn = BaseHook.get_connection(id_conexao)

    # Ajuste do prefixo da URI para o PostgreSQL
    uri = conn.get_uri().replace("postgres:/", "postgresql:/")

    return uri