from airflow.models import DagBag


def test_dags_nao_possuem_erros_importacao():
    """Verifica se existe algum erro de importacao nos DAGs."""
    dag_bag = DagBag(include_examples=False)
    assert len(dag_bag.import_errors) == 0


def test_catavento_postgresql_dependencias_extracao():
    """Task de extracao deve ter como sucessora a task de indexacao."""
    dag = DagBag().get_dag('metadados_postgres_dag')
    task = dag.get_task('extracao_metadados_postgres')
    assert task.downstream_task_ids == {'indexacao_metadados_postgres'}
    assert task.upstream_task_ids == set()


def test_catavento_postgresql_dependencias_indexacao():
    """Task de indexacao deve ter como antecessora a task de extracao."""
    dag = DagBag().get_dag('metadados_postgres_dag')
    task = dag.get_task('indexacao_metadados_postgres')
    assert task.downstream_task_ids == set()
    assert task.upstream_task_ids == {'extracao_metadados_postgres'}
