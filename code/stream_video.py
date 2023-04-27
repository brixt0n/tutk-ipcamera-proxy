#!/usr/bin/env python3
from tutk_wrapper import wrapper
import argparse
import logging

def get_args() -> dict:
    parser = argparse.ArgumentParser()

    # add mutually exclusive group for quiet
    parser.add_argument(
        '-v',
        '--verbose',
        required=False,
        action='store_true',
        default=False,
        help='change logging verbosity to DEBUG')
    
    parser.add_argument(
        '-f',
        '--filename',
        required=True,
        type=argparse.FileType(mode='wb', bufsize=0),
        help='file to write to; use - for stdout')
    
    return parser.parse_args()

def init_logging(verbose: bool = False) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format='%(asctime)s [%(levelname)s] [%(name)s.%(funcName)s]: \
            %(message)s')

if __name__ == "__main__":
    args = get_args()
    init_logging(args.verbose)

    wrapper.initialise()