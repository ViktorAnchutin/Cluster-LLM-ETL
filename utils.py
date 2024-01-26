import htcondor
import os
from htcondor import dags

def create_extract_job():
    extract_job = htcondor.Submit({
    "executable": "run_extract.sh",
    "arguments": "$(input_file) $(output_dir)",
    "output": "extract.out",            
    "error": "extract.err",             
    "log": "extract.log",               
    "request_cpus": "1",               
    "request_memory": "512MB",         
    "request_disk": "128MB",           
    })

    print(f"Extract job: {extract_job}")
    return extract_job

def create_embeddings_job(db_address, db_port, col_name):
    emb_job = htcondor.Submit({
        "executable": "run_embeddings.sh",  
        "arguments": f"$(document) {db_address} {db_port} {col_name}",
        "output": "emb.out",            
        "error": "emb.err",             
        "log": "emb.log",               
        "request_cpus": "1",                
        "request_memory": "512MB",          
        "request_disk": "128MB",     
        "should_transfer_files": "No"       
    })

    print(f"Embeddings job: {emb_job}")
    return emb_job    

def mk_dirs(working_dirs):
    for dir in working_dirs:
        os.mkdir(dir)
        os.chmod(dir,777)


def split_file(input_file, output_dirs, output_name):

    with open(input_file, 'r') as file:
        lines = file.readlines()

    total_lines = len(lines)

    lines_per_file = (total_lines+len(output_dirs)-1)//len(output_dirs)

    for i in range(len(output_dirs)):
        output_file = f"{output_dirs[i]}/{output_name}"

        with open(output_file, 'w') as file:
            start_id = i*lines_per_file
            end_id = min((i+1)*lines_per_file, total_lines)
            file.writelines(lines[start_id:end_id])


def build_dag(extract_job, emb_job, n_par, input_file):
    dag = dags.DAG()    

    working_dirs = [f'pipeline_{i}' for i in range(n_par)]
    mk_dirs(working_dirs)

    split_file_name = "input.txt"
    split_file(input_file,working_dirs,split_file_name)

    extract_vars = [{"input_file":f"{wd}/{split_file_name}", "output_dir":wd} for wd in working_dirs]

    extract_layer = dag.layer(
        name = 'extract',
        submit_description = extract_job,
        vars = extract_vars
    )

    transcript_file_name = "transcripts.json"
    embeddings_vars = [{"document":f"{wd}/{transcript_file_name}"} for wd in working_dirs]

    extract_layer.child_layer(
        name = 'embeddings',
        submit_description = emb_job,
        edge=dags.edges.OneToOne(),
        vars=embeddings_vars
    )

    return dag

    