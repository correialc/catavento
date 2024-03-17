
from pyhocon import ConfigFactory

from databuilder.extractor.postgres_metadata_extractor import PostgresMetadataExtractor
from databuilder.extractor.sql_alchemy_extractor import SQLAlchemyExtractor
from databuilder.job.job import DefaultJob
from databuilder.loader.file_system_neo4j_csv_loader import FsNeo4jCSVLoader
from databuilder.publisher import neo4j_csv_publisher
from databuilder.publisher.neo4j_csv_publisher import Neo4jCsvPublisher
from databuilder.task.task import DefaultTask

from utils import get_conexao_airflow, get_info_conexao_neo4j

SUPPORTED_SCHEMAS = ['public']
SUPPORTED_SCHEMA_SQL_IN_CLAUSE = "('{schemas}')".format(schemas="', '".join(SUPPORTED_SCHEMAS))

NOME_CONEXAO_POSTGRES = "CONEXAO_METADADOS_POSTGRES"


def extrair_metadados_postgres():
    where_clause_suffix = f'st.schemaname in {SUPPORTED_SCHEMA_SQL_IN_CLAUSE}'

    tmp_folder = '/var/tmp/amundsen/table_metadata'
    node_files_folder = f'{tmp_folder}/nodes/'
    relationship_files_folder = f'{tmp_folder}/relationships/'

    string_conexao_postgres = get_conexao_airflow(NOME_CONEXAO_POSTGRES)
    conexao_neo4j = get_info_conexao_neo4j()

    job_config = ConfigFactory.from_dict({
        f'extractor.postgres_metadata.{PostgresMetadataExtractor.WHERE_CLAUSE_SUFFIX_KEY}': where_clause_suffix,
        f'extractor.postgres_metadata.{PostgresMetadataExtractor.USE_CATALOG_AS_CLUSTER_NAME}': True,
        f'extractor.postgres_metadata.extractor.sqlalchemy.{SQLAlchemyExtractor.CONN_STRING}': string_conexao_postgres,
        f'loader.filesystem_csv_neo4j.{FsNeo4jCSVLoader.NODE_DIR_PATH}': node_files_folder,
        f'loader.filesystem_csv_neo4j.{FsNeo4jCSVLoader.RELATION_DIR_PATH}': relationship_files_folder,
        f'publisher.neo4j.{neo4j_csv_publisher.NODE_FILES_DIR}': node_files_folder,
        f'publisher.neo4j.{neo4j_csv_publisher.RELATION_FILES_DIR}': relationship_files_folder,
        f'publisher.neo4j.{neo4j_csv_publisher.NEO4J_END_POINT_KEY}': conexao_neo4j["endpoint"],
        f'publisher.neo4j.{neo4j_csv_publisher.NEO4J_USER}': conexao_neo4j["usuario"],
        f'publisher.neo4j.{neo4j_csv_publisher.NEO4J_PASSWORD}': conexao_neo4j["senha"],
        f'publisher.neo4j.{neo4j_csv_publisher.JOB_PUBLISH_TAG}': 'metadados_postgresql',
    })
    job = DefaultJob(conf=job_config,
                     task=DefaultTask(extractor=PostgresMetadataExtractor(), loader=FsNeo4jCSVLoader()),
                     publisher=Neo4jCsvPublisher())
    job.launch()



