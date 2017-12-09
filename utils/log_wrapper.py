"""
Python wrapper for use with the airflow DataFlowPythonOperator

This gives you a way to execute an external command and still capture logging output
"""

import argparse
import subprocess
import sys
import os
import posixpath as pp
import logging


def get_logger(options):
    if options.startup_log_file:
        try:
            os.makedirs(pp.dirname(options.startup_log_file))
        except os.error:
            pass # directory already exists
        logging.basicConfig(filename=options.startup_log_file)
    else:
        logging.basicConfig()
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    return logger


def run(args):

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--command',
                        required=True,
                        help='command to execute in a subprocess')
    parser.add_argument('--startup_log_file',
                        help='path to write startup output to (default to stdout)')

    options, args = parser.parse_known_args(args)
    command = options.command.split()
    logger = get_logger(options)

    p = subprocess.Popen(command + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    logger.info("Command:\n\n" + "\n  ".join(command + args) + "\n")
    if stderr:
        logger.info("Captured stderr:\n\n" + stderr)
    logger.info("Captured stdout:\n\n" + stdout)

    sys.exit(p.returncode)


if __name__ == '__main__':
    run(sys.argv[1:])