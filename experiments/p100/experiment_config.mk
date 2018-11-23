# Variables for Batch AI - change as necessary
VM_SIZE:=Standard_NC24rs_v2
GPU_TYPE:=p100
CLUSTER_NAME:=pytorchbaitbench${GPU_TYPE}
EXPERIMENT:=experiment_${GPU_TYPE}_${MODEL}
