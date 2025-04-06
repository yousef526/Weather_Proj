from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from WeatherScripts.API_Call import apiCall
from WeatherScripts.producer import produceTopic
from WeatherScripts.spark_Weather import processData
from WeatherScripts.cassandra_creator import create_schema
#from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 8, 1),
    #'retries': 1,
}


# Define the DAG
with DAG(
    dag_id='Weather_Proj',
    default_args=default_args,
    description='A simple weather readings gathering Proj to collect the data of 30 cities in Egypt',
    schedule_interval=timedelta(minutes=40),  # Run once a day
    catchup=False,  # to prevent the dag from trying to run agian and catch days it didnt run
) as dag:

    # Define the Bash task
    task1 = PythonOperator(
        task_id='Produce_data',
        python_callable=apiCall,
        
    )


    task2 = PythonOperator(
        task_id='Write_data_in_kafka',
        python_callable=produceTopic,
        op_args=["/opt/airflow/dags/WeatherScripts/data.json"]
        
    )

    task3 = PythonOperator(
        task_id="Create_Cassandra_schema",
        python_callable=create_schema
    )

    task4 = PythonOperator(
        task_id='Spark_Processing',
        python_callable=processData,
    )


    
    task1 >> task2 >> task3 >> task4

    

    # You can add more tasks here and set dependencies

# You can add dependencies between tasks like this:
# task1 >> task2
    """ task4 = SparkSubmitOperator(
        task_id='Spark_Processing',
        application='/opt/airflow/dags/CryptoScripts/Spark_Processing.py',
        conn_id='spark_default',  # لازم تعرّف Conn ID في Airflow
        verbose=True,
        conf={"spark.master": "spark://spark:7077"},
    ) """