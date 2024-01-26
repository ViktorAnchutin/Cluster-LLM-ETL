#!/bin/bash

input_file=$1
database_address=$2
database_port=$3
collection_name=$4


sudo docker run -v /home/ubuntu/data/Cluster-LLM-ETL:/app/data viktoranchutin/embeddings data/$input_file $database_address $database_port $collection_name
