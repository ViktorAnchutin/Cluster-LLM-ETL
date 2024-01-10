#!/bin/bash

sudo docker run -v /home/ubuntu/data/Cluster-LLM-ETL:/app/data viktoranchutin/embeddings data/parallel_dag/path2/transcripts.json 34.224.15.87 80 parallel_run
