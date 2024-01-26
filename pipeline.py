from htcondor import dags
import os
import configparser
from utils import *

def main():
    print(os.getcwd())
    config = configparser.ConfigParser()
    config.read('config.ini')
    videos_path = config.get("def",'videos_list')
    database_address=config.get("def",'database_address')
    database_port=config.get("def",'database_port')
    collection_name=config.get("def",'collection_name')
    n_par = int(config.get('def','parallel_pipelines'))

    extract_job = create_extract_job()
    emb_job = create_embeddings_job(database_address, database_port, collection_name)
    dag = build_dag(extract_job, emb_job,n_par,videos_path)
    dags.write_dag(dag, ".")


if __name__ == "__main__":
    main()
