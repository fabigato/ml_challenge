import configargparse
import json
# Make sure we can import from folders at the same level inside src (e.g. from scripts folder)
import _init_paths  # noqa: F401


def prColor(text_to_print, color='green', style='reset', do_print=True):
    """
    Create colored text for use in terminal.
    Inspired by comments on this post: https://stackoverflow.com/questions/287871/print-in-terminal-with-colors

    Params:
    - text_to_print: text to print
    - color: string defining which color to use, as listed below
    - style: string defining which style is used for the font
    - do_print: if True, print will be called, if not ANSI formatted text is returned
    """
    colors_dict = {
        'grey': '\033[90m',
        'darkred': '\033[31m',
        'red': '\033[91m',
        'darkgreen': '\033[32m',
        'green': '\033[92m',
        'darkyellow': '\033[33m',
        'yellow': '\033[93m',
        'darkblue': '\033[34m',
        'blue': '\033[94m',
        'darkviolet': '\033[35m',
        'violet': '\033[95m',
        'darkcyan': '\033[36m',
        'cyan': '\033[96m',
    }
    style_dict = {
        'reset': '\033[0m',  # regular font
        'bold': '\033[01m',
        'italic': '\033[03m',
        'underline': '\033[04m',
        'reverse': '\033[07m',  # invert foreground and background color
        'strikethrough': '\033[09m',
        'invisible': '\033[08m'
    }
    color_string = style_dict[style] + colors_dict[color] + "{}\033[00m".format(text_to_print)
    if do_print is True:
        print(color_string)
    return color_string


def str2bool(v):
    """
    Use this function as type for command line options to be used as bool
    """
    if v.lower() in ('yes', 'true', 't', 'y', '1', 'True'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0', 'False'):
        return False
    else:
        raise configargparse.ArgumentTypeError('Boolean value expected.')


def convert_yaml_list_from_config_to_list(config_list):
    """
    Use this function as to convert lists of integers defined in yaml files used in config file parameters
    """
    try:
        # this works when a simple list is used
        converted_list = [eval(i) for i in config_list]
    except SyntaxError:
        reconstructed_string = "["
        for p in config_list:
            reconstructed_string += p + ","
        reconstructed_string = reconstructed_string[:-1] + "]"
        try:
            converted_list = json.loads(reconstructed_string)
        except json.decoder.JSONDecodeError:
            prColor("Cannot convert config {} to list".format(config_list), color="red")
            raise
    return converted_list
