#!/bin/bash

sudo docker run -v /home/ubuntu/data/Cluster-LLM-ETL:/app/data viktoranchutin/extract_subtitles:01 data/test_data/videos_example.txt data
