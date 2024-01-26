#!/bin/bash

input_data=$1
output_dir=$2

sudo docker run -v /home/ubuntu/data/Cluster-LLM-ETL:/app/data viktoranchutin/extract_subtitles:01 data/$input_data data/$output_dir
