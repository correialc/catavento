from utils import get_conexao_airflow
from extracao_postgresql import NOME_CONEXAO_POSTGRES

def test_get_conexao_airflow_formato_uri() -> None:
    """Deve retornar uma conexao Airflow em formato URI."""
    assert get_conexao_airflow(NOME_CONEXAO_POSTGRES).startswith('postgresql:/')



