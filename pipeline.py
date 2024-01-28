from htcondor import dags
import os
import configparser
from utils import *

def main():
    #read config
    config = configparser.ConfigParser()
    config.read('config.ini')
    videos_path = config.get("def",'videos_list')
    database_address=config.get("def",'database_address')
    database_port=config.get("def",'database_port')
    collection_name=config.get("def",'collection_name')
    n_par = int(config.get('def','parallel_pipelines'))

    #create jobs and dag
    extract_job = create_extract_job()
    emb_job = create_embeddings_job(database_address, database_port, collection_name)
    dag = build_dag(extract_job, emb_job,n_par,videos_path)
    
    #submit dag
    dag_file=dags.write_dag(dag, ".")
    dag_submit = htcondor.Submit.from_dag(str(dag_file), {'force': 1})
    schedd = htcondor.Schedd()
    schedd.submit(dag_submit).cluster()


if __name__ == "__main__":
    main()
