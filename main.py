import sys
from argparse import ArgumentError, ArgumentParser


class InputArgumentError(Exception):
    pass


def parse_args(argv):
    try:
        argparser = ArgumentParser(exit_on_error=False)
        argparser.add_argument('-f', '--filepath', type=str)  # temporary solution, rewrite
        args = argparser.parse_args(argv[1:])
    except ArgumentError as e:
        raise InputArgumentError(f"\nНеверно указан параметр."
                                 f"\nНеправильный параметр: {e.argument_name} "
                                 f"\nОшибка, связанная с ним: {e}")
    return args


def main(argv):
    parse_args(argv.filepath)
    pass


if __name__ == "__main__":
    input_arguments = parse_args(sys.argv)
    main(input_arguments)
