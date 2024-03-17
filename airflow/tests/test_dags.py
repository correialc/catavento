import pytest
from airflow.models import DagBag


def test_dags_nao_possuem_erros_importacao():
    """Verifica se existe algum erro de importacao nos DAGs."""
    dag_bag = DagBag(include_examples=False)
    assert len(dag_bag.import_errors) == 0
    assert len(dag_bag.dags) == 2

@pytest.mark.parametrize(('dag_id', 'task_extracao'), [
    ('metadados_postgres_dag', 'extracao_metadados_postgres'),
    ('metadados_mysql_dag', 'extracao_metadados_mysql'),
])
def test_catavento_dependencias_extracao(dag_id: str, task_extracao: str):
    """Task de extracao deve ter como sucessora a task de indexacao."""
    dag = DagBag().get_dag(dag_id)
    task = dag.get_task(task_extracao)
    assert task.downstream_task_ids == {'indexacao_metadados'}
    assert task.upstream_task_ids == set()


@pytest.mark.parametrize(('dag_id', 'task_extracao'), [
    ('metadados_postgres_dag', 'extracao_metadados_postgres'),
    ('metadados_mysql_dag', 'extracao_metadados_mysql'),
])
def test_catavento_dependencias_indexacao(dag_id: str, task_extracao: str):
    """Task de indexacao deve ter como antecessora a task de extracao."""
    dag = DagBag().get_dag(dag_id)
    task = dag.get_task('indexacao_metadados')
    assert task.downstream_task_ids == set()
    assert task.upstream_task_ids == {task_extracao}


