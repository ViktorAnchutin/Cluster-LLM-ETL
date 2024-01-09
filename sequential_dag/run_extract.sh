#!/bin/bash

sudo docker run -v /home/ubuntu/data/Cluster-LLM-ETL:/app/data viktoranchutin/extract_subtitles:01 data/input/all_videos.txt data
