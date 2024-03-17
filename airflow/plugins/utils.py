from typing import Dict

from airflow.hooks.base_hook import BaseHook
from airflow.models import Variable

def get_conexao_airflow(id_conexao: str) -> str:
    """Retorna uma conexao (formato RI) armazenada previamente no Airflow."""
    conn = BaseHook.get_connection(id_conexao)

    # Ajuste do prefixo da URI para o PostgreSQL
    uri = conn.get_uri().replace("postgres:/", "postgresql:/")

    return uri

def get_info_conexao_neo4j() -> Dict[str, str]:
    """Retorna dados de conexao com o NEO4J."""
    return {
        'endpoint': Variable.get('neo4j_endpoint'),
        'usuario': Variable.get('neo4j_usuario'),
        'senha': Variable.get('neo4j_senha'),
    }