# Variables for Batch AI - change as necessary
VM_SIZE:=Standard_NC24r
GPU_TYPE:=k80
CLUSTER_NAME:=pytorchbaitbench${GPU_TYPE}
EXPERIMENT:=experiment_${GPU_TYPE}_${MODEL}
