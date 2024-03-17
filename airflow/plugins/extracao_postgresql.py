import uuid

from pyhocon import ConfigFactory

from elasticsearch import Elasticsearch
from databuilder.extractor.neo4j_extractor import Neo4jExtractor
from databuilder.extractor.neo4j_search_data_extractor import Neo4jSearchDataExtractor
from databuilder.extractor.postgres_metadata_extractor import PostgresMetadataExtractor
from databuilder.extractor.sql_alchemy_extractor import SQLAlchemyExtractor
from databuilder.job.job import DefaultJob
from databuilder.loader.file_system_elasticsearch_json_loader import FSElasticsearchJSONLoader
from databuilder.loader.file_system_neo4j_csv_loader import FsNeo4jCSVLoader
from databuilder.publisher import neo4j_csv_publisher
from databuilder.publisher.elasticsearch_publisher import ElasticsearchPublisher
from databuilder.publisher.neo4j_csv_publisher import Neo4jCsvPublisher
from databuilder.task.task import DefaultTask
from databuilder.transformer.base_transformer import NoopTransformer

from utils import get_conexao_airflow

NEO4J_ENDPOINT = 'bolt://neo4j_amundsen:7687'
neo4j_endpoint = NEO4J_ENDPOINT
neo4j_user = 'neo4j'
neo4j_password = 'test'

es = Elasticsearch([
    {'host': 'elasticsearch'},
])

SUPPORTED_SCHEMAS = ['public']
SUPPORTED_SCHEMA_SQL_IN_CLAUSE = "('{schemas}')".format(schemas="', '".join(SUPPORTED_SCHEMAS))
OPTIONAL_TABLE_NAMES = ''

NOME_CONEXAO_POSTGRES = "CONEXAO_METADADOS_POSTGRES"

def extrair_metadados_postgres():
    where_clause_suffix = f'st.schemaname in {SUPPORTED_SCHEMA_SQL_IN_CLAUSE}'

    tmp_folder = '/var/tmp/amundsen/table_metadata'
    node_files_folder = f'{tmp_folder}/nodes/'
    relationship_files_folder = f'{tmp_folder}/relationships/'

    string_conexao_postgres = get_conexao_airflow(NOME_CONEXAO_POSTGRES)

    job_config = ConfigFactory.from_dict({
        f'extractor.postgres_metadata.{PostgresMetadataExtractor.WHERE_CLAUSE_SUFFIX_KEY}': where_clause_suffix,
        f'extractor.postgres_metadata.{PostgresMetadataExtractor.USE_CATALOG_AS_CLUSTER_NAME}': True,
        f'extractor.postgres_metadata.extractor.sqlalchemy.{SQLAlchemyExtractor.CONN_STRING}': string_conexao_postgres,
        f'loader.filesystem_csv_neo4j.{FsNeo4jCSVLoader.NODE_DIR_PATH}': node_files_folder,
        f'loader.filesystem_csv_neo4j.{FsNeo4jCSVLoader.RELATION_DIR_PATH}': relationship_files_folder,
        f'publisher.neo4j.{neo4j_csv_publisher.NODE_FILES_DIR}': node_files_folder,
        f'publisher.neo4j.{neo4j_csv_publisher.RELATION_FILES_DIR}': relationship_files_folder,
        f'publisher.neo4j.{neo4j_csv_publisher.NEO4J_END_POINT_KEY}': neo4j_endpoint,
        f'publisher.neo4j.{neo4j_csv_publisher.NEO4J_USER}': neo4j_user,
        f'publisher.neo4j.{neo4j_csv_publisher.NEO4J_PASSWORD}': neo4j_password,
        f'publisher.neo4j.{neo4j_csv_publisher.JOB_PUBLISH_TAG}': 'metadados_postgresql',
    })
    job = DefaultJob(conf=job_config,
                     task=DefaultTask(extractor=PostgresMetadataExtractor(), loader=FsNeo4jCSVLoader()),
                     publisher=Neo4jCsvPublisher())
    job.launch()


def indexar_metadados_postgres():
    extracted_search_data_path = '/var/tmp/amundsen/search_data.json'

    task = DefaultTask(loader=FSElasticsearchJSONLoader(),
                       extractor=Neo4jSearchDataExtractor(),
                       transformer=NoopTransformer())

    elasticsearch_client = es
    elasticsearch_new_index_key = f'tables{uuid.uuid4()}'
    elasticsearch_new_index_key_type = 'table'
    elasticsearch_index_alias = 'table_search_index'

    job_config = ConfigFactory.from_dict({
        f'extractor.search_data.extractor.neo4j.{Neo4jExtractor.GRAPH_URL_CONFIG_KEY}': neo4j_endpoint,
        f'extractor.search_data.extractor.neo4j.{Neo4jExtractor.MODEL_CLASS_CONFIG_KEY}':
            'databuilder.models.table_elasticsearch_document.TableESDocument',
        f'extractor.search_data.extractor.neo4j.{Neo4jExtractor.NEO4J_AUTH_USER}': neo4j_user,
        f'extractor.search_data.extractor.neo4j.{Neo4jExtractor.NEO4J_AUTH_PW}': neo4j_password,
        f'loader.filesystem.elasticsearch.{FSElasticsearchJSONLoader.FILE_PATH_CONFIG_KEY}': extracted_search_data_path,
        f'loader.filesystem.elasticsearch.{FSElasticsearchJSONLoader.FILE_MODE_CONFIG_KEY}': 'w',
        f'publisher.elasticsearch.{ElasticsearchPublisher.FILE_PATH_CONFIG_KEY}': extracted_search_data_path,
        f'publisher.elasticsearch.{ElasticsearchPublisher.FILE_MODE_CONFIG_KEY}': 'r',
        f'publisher.elasticsearch.{ElasticsearchPublisher.ELASTICSEARCH_CLIENT_CONFIG_KEY}':
            elasticsearch_client,
        f'publisher.elasticsearch.{ElasticsearchPublisher.ELASTICSEARCH_NEW_INDEX_CONFIG_KEY}':
            elasticsearch_new_index_key,
        f'publisher.elasticsearch.{ElasticsearchPublisher.ELASTICSEARCH_DOC_TYPE_CONFIG_KEY}':
            elasticsearch_new_index_key_type,
        f'publisher.elasticsearch.{ElasticsearchPublisher.ELASTICSEARCH_ALIAS_CONFIG_KEY}':
            elasticsearch_index_alias
    })

    job = DefaultJob(conf=job_config,
                     task=task,
                     publisher=ElasticsearchPublisher())
    job.launch()
