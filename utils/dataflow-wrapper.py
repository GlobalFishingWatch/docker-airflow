"""
Python wrapper for use with the airflow DataFlowPythonOperator

This gives you a way to execute a python file and still capture logging output
"""

import argparse
import subprocess
import sys

def launch(args):

    print args
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--startup_log_path',
                        help='path to write startup output to (default to stdout)')
    parser.add_argument('--command',
                        help='command to execute in a subprocess')

    options, args = parser.parse_known_args(args)
    command = options.command.split()
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    # logfile = open('/usr/local/airflow/wrapper.log', 'a')
    logfile = open(options.startup_log_path, 'w') if options.startup_log_path else sys.stdout
    logfile.write("Command:\n\n")
    logfile.write('\n  '.join(command + args))
    logfile.write('\n\n\n')
    logfile.write("Captured stderr:\n\n")
    logfile.write(stderr)
    logfile.write('\n\n')
    logfile.write("Captured stdout:\n\n")
    logfile.write(stdout)
    logfile.write('\n\n')

    # sys.exit(p.returncode)


if __name__ == '__main__':
    launch(sys.argv[1:])