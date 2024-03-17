FROM apache/airflow:2.8.2
ADD requirements.txt .
ADD pytest.ini .
RUN pip install apache-airflow==${AIRFLOW_VERSION} -r requirements.txt
RUN pip install amundsen-databuilder
RUN pip install pytest