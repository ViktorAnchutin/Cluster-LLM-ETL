## Configuration for NFS

Mkae sure that submission host and executors have the same parameters in /etc/condor/condor_config:

UID_DOMAIN = ec2.internal
FILESYSTEM_DOMAIN = wqd7008 # can be anything, but should be the same 

