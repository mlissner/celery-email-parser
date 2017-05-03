import argparse
import os


def readable_dir(prospective_dir):
    if not os.path.isdir(prospective_dir):
        raise argparse.ArgumentTypeError(
            "readable_dir:{0} is not a valid path".format(prospective_dir))
    if os.access(prospective_dir, os.R_OK):
        return prospective_dir
    else:
        raise argparse.ArgumentTypeError(
            "readable_dir:{0} is not a readable dir".format(prospective_dir))
