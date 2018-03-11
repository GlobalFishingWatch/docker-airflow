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
import select


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


def log_line(line, logger):
    # TODO: Should just use another handler in the logger to sent to stdout
    print line
    logger.info(line)


class _Subprocess():
    def __init__(self, cmd, args, logger):
        self.log = logger
        self._proc = subprocess.Popen(cmd + args, shell=False, stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)

    def _line(self, fd):
        if fd == self._proc.stderr.fileno():
            line = self._proc.stderr.readline()
            return line
        if fd == self._proc.stdout.fileno():
            line = self._proc.stdout.readline()
            return line

    def _log_line(self, line):
        log_line(line, self.log)

    def wait_for_done(self):
        reads = [self._proc.stderr.fileno(), self._proc.stdout.fileno()]
        self._log_line("Output:\n")
        while self._proc.poll() is None:
            ret = select.select(reads, [], [], 5)
            if ret is not None:
                for fd in ret[0]:
                    line = self._line(fd)
                    self._log_line(line[:-1])
            else:
                self._log_line("Waiting for DataFlow process to complete.")

        stdout, stderr = self._proc.communicate()
        if stdout:
            self._log_line(stdout)
        if stderr:
            self._log_line(stderr)

        return self._proc.returncode



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

    log_line("####################################", logger)
    log_line("### Begin log wrapper invocation", logger)
    log_line("###\n", logger)
    log_line("Command:\n\n" + "\n  ".join(command + args) + "\n", logger)

    ret_code = _Subprocess(command, args, logger).wait_for_done()

    log_line("### Log Wrapper exiting with return code %s" % ret_code, logger)
    log_line("###", logger)
    log_line("####################################", logger)

    sys.exit(ret_code)


if __name__ == '__main__':
    run(sys.argv[1:])