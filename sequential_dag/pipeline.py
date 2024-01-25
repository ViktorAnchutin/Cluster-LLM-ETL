import htcondor
from htcondor import dags
import os
import configparser

def main():
    print(os.getcwd())
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.sections()

    videos_path = config.get('Extract_Job', 'videos_list')
    output_dir = config.get('Extract_Job', 'output_dir')

    extract_job = htcondor.Submit({
        "executable": "run_extract.sh",
        "arguments": f"{videos_path} {output_dir}",
        "output": "extract.out",            # anything the job prints to standard output will end up in this file
        "error": "extract.err",             # anything the job prints to standard error will end up in this file
        "log": "extract.log",               # this file will contain a record of what happened to the job
        "request_cpus": "1",                # how many CPU cores we want
        "request_memory": "512MB",          # how much memory we want
        "request_disk": "128MB",            # how much disk space we want
        "should_transfer_files": "No"
    })

    print(f"Extract job: {extract_job}")

    document=config.get('Embeddings_Job', 'document')
    database_address=config.get('Embeddings_Job', 'database_address')
    database_port=config.get('Embeddings_Job', 'database_port')
    collection_name=config.get('Embeddings_Job', 'collection_name')

    emb_job = htcondor.Submit({
        "executable": "run_embeddings.sh",  
        "arguments": f"{document} {database_address} {database_port} {collection_name}",
        "output": "emb.out",            
        "error": "emb.err",             
        "log": "emb.log",               
        "request_cpus": "1",                
        "request_memory": "512MB",          
        "request_disk": "128MB",     
        "should_transfer_files": "No"       
    })

    print(f"Embeddings job: {emb_job}")

    dag = dags.DAG()

    extract_layer = dag.layer(
        name = 'extract',
        submit_description = extract_job
    )

    extract_layer.child_layer(
        name = 'emb',
        submit_description = emb_job
    )

    dags.write_dag(dag, ".")


if __name__ == "__main__":
    main()
