define PROJECT_HELP_MSG
Usage:
    make help                   show this message
    make build                  make Horovod Keras image with Open MPI
    make run-mpi				run training using Open MPI image
    make push					push Horovod Keras image with Open MPI
endef
export PROJECT_HELP_MSG


numproc:=2 # Number of precesses/GPUs
name_prefix:=masalvar
tag:=0.15.1 
model:=resnet50

define execute_mpi
 nvidia-docker run -it \
 --privileged \
 $(1) bash -c "mpirun -np $(numproc) -H localhost:$(numproc) -bind-to none \
 			   -map-by slot -x NCCL_DEBUG=INFO \
 			   -x LD_LIBRARY_PATH -x PATH \
 			    -mca pml ob1 -mca btl ^openib \
 			   python /benchmarks/pytorch_synthetic_benchmark.py --model $(model) --batch-size 64"
endef


help:
	echo "$$PROJECT_HELP_MSG" | less

build:
	docker build -t $(name_prefix)/horovod-batchai-pytorch-bench:$(tag) Docker

run-mpi:
	$(call execute_mpi, $(name_prefix)/horovod-batchai-pytorch-bench:$(tag))

push:
	docker push $(name_prefix)/horovod-batchai-pytorch-bench:$(tag)


.PHONY: help build push
