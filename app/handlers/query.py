import os
import sys
import importlib
from inspect import getmembers, isclass


def bootstrap_queries():
    queries_base_classes = []
    current_directory = os.path.dirname(os.path.abspath(__file__))

    subdirectories = []
    for child in os.listdir(current_directory):
        if os.path.isdir(os.path.join(current_directory, child)) and child != '__pycache__':
            subdirectories.append(child)

    for directory in subdirectories:

        try:
            module = importlib.import_module(
                f'.{directory}.queries', package=__package__)

            if module:
                classes = [x for x in getmembers(module, isclass)]
                queries = [x[1] for x in classes if 'Query' in x[0]]
                queries_base_classes += queries
        except ModuleNotFoundError as e:
            print(e, file=sys.stderr)

    properties = {}

    for base_class in queries_base_classes:
        properties.update(base_class.__dict__['_meta'].fields)

    Queries = type(
        'Queries',
        tuple(queries_base_classes),
        properties
    )

    return Queries
