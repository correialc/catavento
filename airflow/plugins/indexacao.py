import uuid

from pyhocon import ConfigFactory

from databuilder.extractor.neo4j_extractor import Neo4jExtractor
from databuilder.extractor.neo4j_search_data_extractor import Neo4jSearchDataExtractor
from databuilder.loader.file_system_elasticsearch_json_loader import FSElasticsearchJSONLoader
from databuilder.publisher.elasticsearch_publisher import ElasticsearchPublisher
from databuilder.transformer.base_transformer import NoopTransformer
from databuilder.job.job import DefaultJob
from databuilder.task.task import DefaultTask

from elasticsearch import Elasticsearch

from utils import get_info_conexao_neo4j

es = Elasticsearch([
    {'host': 'elasticsearch'},
])

def indexar_metadados():
    extracted_search_data_path = '/var/tmp/amundsen/search_data.json'

    task = DefaultTask(loader=FSElasticsearchJSONLoader(),
                       extractor=Neo4jSearchDataExtractor(),
                       transformer=NoopTransformer())

    elasticsearch_client = es
    elasticsearch_new_index_key = f'tables{uuid.uuid4()}'
    elasticsearch_new_index_key_type = 'table'
    elasticsearch_index_alias = 'table_search_index'

    conexao_neo4j = get_info_conexao_neo4j()

    job_config = ConfigFactory.from_dict({
        f'extractor.search_data.extractor.neo4j.{Neo4jExtractor.GRAPH_URL_CONFIG_KEY}': conexao_neo4j["endpoint"],
        f'extractor.search_data.extractor.neo4j.{Neo4jExtractor.MODEL_CLASS_CONFIG_KEY}':
            'databuilder.models.table_elasticsearch_document.TableESDocument',
        f'extractor.search_data.extractor.neo4j.{Neo4jExtractor.NEO4J_AUTH_USER}': conexao_neo4j["usuario"],
        f'extractor.search_data.extractor.neo4j.{Neo4jExtractor.NEO4J_AUTH_PW}': conexao_neo4j["senha"],
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