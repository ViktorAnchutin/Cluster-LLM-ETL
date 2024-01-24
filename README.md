## Project Description

A distributed implementation of the ETL pipeline for vector database. Jobs are run in Docker containers on HTCondor cluster.

I take 2 video playlists from Youtube and load them into vector database.

![](imgs/pic1.png)

## Pipeline overview

### Stage 1: Load and preprocess text 
Transcripts of the videos are fetched from Youtube. The obtained
transcripts are split into chunks. For each chunk a json object is created which contains a URL for the video, the text chunk and the timestamp.

### Stage 2: Create embeddings and load into vector database
The second stage takes the json document and creates vector embeddings for the text
chunks. Embeddings are created with the sentence transformer library [4]. After embeddings
are created, they are loaded into the vector database together with the corresponding json
objects.

## Configuration for NFS

Submission host and executors must have the same parameters in /etc/condor/condor_config:

UID_DOMAIN = ec2.internal

FILESYSTEM_DOMAIN = wqd7008 # can be anything, but should be the same 

