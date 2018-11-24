PWD:=$(shell pwd)

# Variables for Batch AI - change as necessary
ID:=baitbenchpytorch
LOCATION:=eastus
GROUP_NAME:=batch${ID}rg
STORAGE_ACCOUNT_NAME:=batch${ID}st
CONTAINER_NAME:=batch${ID}container
FILE_SHARE_NAME:=batch2${ID}share
NUM_NODES:=8
JOB_NAME:=pytorch_benchmark
SELECTED_SUBSCRIPTION:="Boston Team Danielle"
WORKSPACE:=workspace_0_15_1
PROCESSES_PER_NODE:=4