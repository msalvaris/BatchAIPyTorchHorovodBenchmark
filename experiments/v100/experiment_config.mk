# Variables for Batch AI - change as necessary
VM_SIZE:=Standard_NC24rs_v3
GPU_TYPE:=v100
CLUSTER_NAME:=pytorchbaitbench${GPU_TYPE}
EXPERIMENT:=experiment_${GPU_TYPE}_${MODEL}
