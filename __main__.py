import argparse
import imp
import inspect
import os

from execution import TinyTester
from test      import TestClass


class ChDir(object):

    def __init__(self, newPath):

        self.__newPath = newPath

    def __enter__(self):

        self.__savedPath = os.getcwd()
        os.chdir(self.__newPath)

    def __exit__(self, type, value, traceback):

        os.chdir(self.__savedPath)


def getFiles(directory):

    for file in os.listdir(directory):
        if not file.startswith('_') and os.path.isfile(os.path.join(directory, file)):

            name, ext = os.path.splitext(file)

            if ext == '.py' and not name.startswith('_'):
                yield name


def getTests(directory):

    with ChDir(directory):

        tests = []
        for file in getFiles(directory):

            module = imp.load_source(file, os.path.join(directory, '{0}.py'.format(file)))

            for name, obj in inspect.getmembers(module):

                if inspect.isclass(obj) and obj.__module__ == module.__name__ and issubclass(obj, TestClass):
                    tests.append(obj)

    return tests


####################################################################
#
#   Main
#
####################################################################

def run():

    parser = argparse.ArgumentParser()

    parser.add_argument('--directory', required = False, default = None,   help = 'Location of tests to run. Defaults to current working directory.')
    parser.add_argument('--loglevel',  required = False, default = 'INFO', help = 'The logging level.')

    args = parser.parse_args()

    directory = args.directory if args.directory is not None else os.getcwd()

    TinyTester(level=args.loglevel).run(getTests(directory))


if __name__ == '__main__':
    run()