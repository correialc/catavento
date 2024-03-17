from utils import get_conexao_airflow, get_info_conexao_neo4j
from extracao_postgresql import NOME_CONEXAO_POSTGRES


def test_get_conexao_airflow_formato_uri() -> None:
    """Deve retornar uma conexao Airflow em formato URI."""
    assert get_conexao_airflow(NOME_CONEXAO_POSTGRES).startswith('postgresql:/')


def test_get_info_conexao_neo4j() -> None:
    """Deve retornar dados para conexao com o NEO4J."""
    conexao_neo4j = get_info_conexao_neo4j()
    assert list(conexao_neo4j.keys()) == ['endpoint', 'usuario', 'senha']
    assert conexao_neo4j["endpoint"].startswith("bolt://")

