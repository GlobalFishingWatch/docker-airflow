import logging
from airflow.models import Variable

def set_default_variables(pipeline_name, variables, force=False):
    config = Variable.get(pipeline_name, default_var={}, deserialize_json=True)
    for key, val in variables:
        if force or key not in config:
            config[key] = val
            logging.info("Setting {}:{} to {}".format(pipeline_name, key, val))
        else:
            logging.info("Leaving {}:{} as {}".format(pipeline_name, key, config[key]))
    Variable.set(pipeline_name, config, serialize_json=True)


def create_pairs(seq):
    for x in seq:
        key, val = x.split('=')
        yield (key, val)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Set Airflow defaults for a pipeline')
    parser.add_argument('pipeline_name',
                    help='Name of the pipeline; all variables are entriesin a dict with this name')
    parser.add_argument('--force', action='append', dest='forced',
                        help='forced NAME=DEFAULT value; this *will* override existing entries')
    parser.add_argument('names_with_defaults', nargs='*',
                        help='NAME=DEFAULT values; these *will not* override existing entries')

    args = parser.parse_args()

    set_default_variables(args.pipeline_name, create_pairs(args.names_with_defaults))

    set_default_variables(args.pipeline_name, create_pairs(args.forced), force=True)


