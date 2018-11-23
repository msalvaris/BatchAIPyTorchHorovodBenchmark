import argparse
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#
# Config for Intel
cmd_for_intel =  \
"""source /opt/intel/compilers_and_libraries_2017.4.196/linux/mpi/intel64/bin/mpivars.sh; 
echo $AZ_BATCH_HOST_LIST; 
mpirun -n {total_processes} -ppn {processes_per_node} {hosts}
-env I_MPI_FABRICS=dapl 
-env I_MPI_DAPL_PROVIDER=ofa-v2-ib0 
-env I_MPI_DYNAMIC_CONNECTION=0 
-env I_MPI_DEBUG=6 
-env I_MPI_HYDRA_DEBUG=on 
python /benchmarks/scripts/tf_cnn_benchmarks/tf_cnn_benchmarks.py --model {model} --batch_size 64 --variable_update horovod""".replace('\n', '')

# Config for OpenMPI
cmd_for_openmpi =  \
"""echo $AZ_BATCH_HOST_LIST; 
cat $AZ_BATCHAI_MPI_HOST_FILE; 
mpirun -np {total_processes} 
-bind-to none -map-by slot 
-x NCCL_DEBUG=INFO -x LD_LIBRARY_PATH 
-mca btl_tcp_if_include eth0 
-x NCCL_SOCKET_IFNAME=eth0 
-mca btl ^openib 
-x NCCL_IB_DISABLE=1 
--allow-run-as-root 
{hosts} 
python /benchmarks/scripts/tf_cnn_benchmarks/tf_cnn_benchmarks.py --model {model} --batch_size 64 --variable_update horovod""".replace('\n', '')

# Running on single node without mpi
cmd_local="""python /benchmarks/scripts/tf_cnn_benchmarks/tf_cnn_benchmarks.py --model {model} --batch_size 64""".replace('\n', '')

cmd_choice_dict={
    'openmpi':cmd_for_openmpi,
    'intelmpi':cmd_for_intel,
    'local':cmd_local
}

hosts_param={
    'openmpi':'--hostfile $AZ_BATCHAI_MPI_HOST_FILE ',
    'intelmpi':'-hosts $AZ_BATCH_HOST_LIST ',
    'local': ''
}

def _hosts_for(mpitype, node_count):
    if node_count>1:
        return hosts_param.get(mpitype, '')
    else:
        return hosts_param.get('local')


def generate_job_dict(image_name,
                      mpitype,
                      node_count=2,
                      model='resnet50',
                      total_processes=None,
                      processes_per_node=4):
    total_processes = processes_per_node*node_count if total_processes is None else total_processes
    command = cmd_choice_dict.get(mpitype, cmd_for_intel)

    return {
        "$schema": "https://raw.githubusercontent.com/Azure/BatchAI/master/schemas/2017-09-01-preview/job.json",
        "properties": {
            "nodeCount": node_count,
            "customToolkitSettings": {
                "commandLine": command.format(total_processes=total_processes,
                                              processes_per_node=processes_per_node,
                                              model=model,
                                              hosts=_hosts_for(mpitype, node_count) )
            },
            "stdOutErrPathPrefix": "$AZ_BATCHAI_MOUNT_ROOT/extfs",
            "containerSettings": {
                "imageSourceRegistry": {
                    "image": image_name
                }
            }
        }
    }


def write_json_to_file(json_dict, filename, mode='w'):
    with open(filename, mode) as outfile:
        json.dump(json_dict, outfile, indent=4,sort_keys=True)
        outfile.write('\n\n')


def main(image_name,
         mpitype,
         filename='job.json',
         node_count=2,
         model='resnet50',
         total_processes=None,
         processes_per_node=4):
    logger.info('Creating manifest {} with {} image...'.format(filename, image_name))
    job_template = generate_job_dict(image_name,
                                     mpitype,
                                     node_count=node_count,
                                     model=model,
                                     total_processes=total_processes,
                                     processes_per_node=processes_per_node)
    write_json_to_file(job_template, filename)
    logger.info('Done')


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Generate manifest')
    parser.add_argument('docker_image', type=str,
                        help='docker image to use')
    parser.add_argument('mpi', type=str,
                        help='mpi to use, must be install in the docker image provided options:[intelmpi, openmpi, local]')
    parser.add_argument('--filename', '-f', dest='filename', type=str, nargs='?',
                        default='job.json',
                        help='name of the file to save job spec to')
    parser.add_argument('--node_count', '-n', dest='node_count', type=int, nargs='?',
                        default=1, help='the number of nodes to run the job across')
    parser.add_argument('--model', '-m', dest='model', type=str, nargs='?',
                        default='resnet50',
                        help='the model to use')
    parser.add_argument('--ppn', dest='processes_per_node', type=int, nargs='?',
                        default=4,
                        help='number of GPU proceses to run per node')
    args = parser.parse_args()
    main(args.docker_image,
         args.mpi,
         filename=args.filename,
         node_count=args.node_count,
         model=args.model,
         processes_per_node=args.processes_per_node)