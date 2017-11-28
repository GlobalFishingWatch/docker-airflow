"""
Stub to run Python Dataflow inside a docker container
(Meant to be used with airflow)

Usage:

Python dataflow_docker_stub.py \
    --startup_log_path=LOG_PATH \
    --docker_image=IMAGE_NAME \
    --gcp_volume=VOLUME_NAME \
    --python_module=MODULE_NAME
    ARGS_FOR_PYTHON MODULE...

This runs the specified module inside the image. The gcp_volume
directory is mounted for Google authentification. All 
other arguments are passed along to the python module
inside the docker module.

Note that that `gcp_volume` may differ from what is seen in
`docker-compose.yaml` since `docker-compose` prepends
the directory name (or project name if specified) to the name
used in `docker-compose.yaml`.

Stdout and stderr are captured and logged to LOG_PATH, or
stdout if that is ommitted. The logs are accumulated in 
memory, so if we start accumulating enormous logs, we'll 
have to rework the way that is done.

Here are a couple of examples I've been using for testing locally.


python dataflow_docker_stub.py \
    --docker_image=gfw/pipe-anchorages \
    --gcp_volume=anchorages_gcp \
    --python_module=pipe_anchorages.port_events \
    --job_name portvisitsoneday \
    --anchorage_table gfw_raw.anchorage_naming_20171026 \
    --start_date 2016-01-01 \
    --end_date 2016-01-01 \
    --output_table machine_learning_dev_ttl_30d.in_out_events_test \
    --project world-fishing-827 \
    --max_num_workers 100 \
    --requirements_file requirements.txt \
    --project world-fishing-827 \
    --staging_location gs://machine-learning-dev-ttl-30d/anchorages/portevents/output/staging \
    --temp_location gs://machine-learning-dev-ttl-30d/anchorages/temp \
    --setup_file ./setup.py \
    --runner DataflowRunner \
    --disk_size_gb 100

python dataflow_docker_stub.py \
    --startup_log_path=startup_log.txt \
    --docker_image=gfw/pipe-anchorages \
    --gcp_volume=anchorages_gcp \
    --python_module=pipe_anchorages.port_events \
    --help


"""
import argparse
import subprocess
import sys

def launch(args):
    # Use add_help=False so that underlying module can pass back help.
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--startup_log_path', 
                        help='path to write startup output to (default to stdout)')
    parser.add_argument('--docker_image',
                        required=True,
                        help='name of docker image to invoke')
    parser.add_argument('--gcp_volume',
                        required=True,
                        help='name of volume with Google Cloud Platform credentials installed') 
    parser.add_argument('--python_module',
                        required=True,
                        help='command to be invoked in docker')

    options, docker_args = parser.parse_known_args()

    command = ['docker', 'run', '-v', '{}:/root/.config/'.format(options.gcp_volume), 
            options.docker_image, 'python', '-m', options.python_module] + docker_args

    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    logfile = open(options.startup_log_path, 'a') if options.startup_log_path else sys.stdout
    try:
        logfile.write("Command:\n\n")
        logfile.write(' '.join(command))
        logfile.write('\n\n\n')
        logfile.write("Captured stderr:\n\n")
        logfile.write(stderr)
        logfile.write('\n\n')
        logfile.write("Captured stdout:\n\n")
        logfile.write(stdout)
        logfile.write('\n\n')
    finally:
        if options.startup_log_path:
            logfile.close()

    sys.exit(p.returncode)


if __name__ == '__main__':
    launch(sys.argv)