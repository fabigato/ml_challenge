"""
Script doing XXX

Example call using parameter file:
python empty_script.py -c=../../experiments_configs/empty_script_config.yaml'
"""
import os
import configargparse

# Make sure we can import from folders at the same level inside src (e.g. from scripts folder)
import _init_paths  # noqa: F401

from utils.simple_utils import prColor, str2bool, convert_yaml_list_from_config_to_list


def run_example(input_data_filename, output_folder, example_bool, example_list):

    # If output folder is provided use it, otherwise use same folder as input file
    if output_folder is not None:
        saving_path = output_folder
    else:
        saving_path = os.path.split(input_data_filename)[0] + '/'

    # Create output folder
    if not os.path.isdir(saving_path):
        os.mkdir(saving_path)
    prColor("test green print")

    print("This is an example bool: {}".format(example_bool))
    print("This is an example list: {}".format(example_list))


if __name__ == '__main__':
    p = configargparse.ArgParser()

    p.add('-c', '--config', required=False,
          is_config_file=True, help='Script doing XXX')
    # options can be set in a config file because it starts with '--'

    p.add('-f', '--file', help='Input file')
    p.add('-of', '--outputfolder', help='folder in which to save data', default=None)
    # In order to properly convert a list from a yaml file you will need to define it as a str, use nargs='+'
    # AND use convert_yaml_list_from_config_to_list to convert its values
    p.add('--example_list', type=str, nargs='+', help='example of how to import list in yaml files', default=None)
    p.add('--example_bool', type=str2bool, help='example of how to import bools in yaml files', default=None)

    str2bool, convert_yaml_list_from_config_to_list
    options = p.parse_args()

    if options.file is None:
        print("Input file is required.")
        p.print_help()
        print("python src/scripts/empty_script.py -f=test.txt -of=./output/")
        print("python src/scripts/empty_script.py -c=./experiments_configs/empty_script_config.yaml")
    else:
        run_example(options.file, options.outputfolder, options.example_bool,
                    convert_yaml_list_from_config_to_list(options.example_list))
