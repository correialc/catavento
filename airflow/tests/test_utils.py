import pytest

from utils import get_conexao_airflow, get_info_conexao_neo4j
from extracao_postgresql import NOME_CONEXAO_POSTGRES
from extracao_mysql import NOME_CONEXAO_MYSQL


@pytest.mark.parametrize(('nome_conexao', 'prefixo_conexao'), [
    (NOME_CONEXAO_POSTGRES, 'postgresql://'),
    (NOME_CONEXAO_MYSQL, 'mysql://'),
])
def test_get_conexao_airflow_formato_uri(nome_conexao: str, prefixo_conexao: str) -> None:
    """Deve retornar uma conexao Airflow em formato URI."""
    assert get_conexao_airflow(nome_conexao).startswith(prefixo_conexao)


def test_get_info_conexao_neo4j() -> None:
    """Deve retornar dados para conexao com o NEO4J."""
    conexao_neo4j = get_info_conexao_neo4j()
    assert list(conexao_neo4j.keys()) == ['endpoint', 'usuario', 'senha']
    assert conexao_neo4j["endpoint"].startswith("bolt://")

