#!/bin/bash

sudo docker run -v /home/ubuntu/data/Cluster-LLM-ETL:/app/data viktoranchutin/embeddings data/sequential_dag/transcripts.json 34.224.15.87 80 seq_run
