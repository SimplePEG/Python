import os
from os import path as op


def read_file(filename):
    with open(filename, 'r') as fd:
        return fd.read()


def collect_files(root, predicate=lambda x: True):
    return [
        op.join(root, f)
        for f in os.listdir(root)
        if predicate(f)]
