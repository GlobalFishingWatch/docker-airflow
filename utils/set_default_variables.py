from airflow.models import Variable

def set_default_variables(pipeline_name, variables):
    config = Variable.get(pipeline_name, default_var={}, deserialize_json=True)
    for key, val in variables:
        if key not in config:
            config[key] = val
    print("Setting to {} to {}".format(pipeline_name, config))
    Variable.set(pipeline_name, config, serialize_json=True)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Set Airflow defaults for a pipeline')
    parser.add_argument('pipeline_name',
                    help='an integer for the accumulator')
    parser.add_argument('names_with_defaults', nargs='*',
                        help='NAME=DEFAULT values')

    args = parser.parse_args()

    variables = []
    for x in args.names_with_defaults:
        key, val = x.split('=')
        variables.append((key, val))

    set_default_variables(args.pipeline_name, variables)
