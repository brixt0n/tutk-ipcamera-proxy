#!/usr/bin/env python3
from tutk_proxy import proxy
import argparse
import logging
from tutk_proxy.models import (
    TutkDevice
)

log = logging.getLogger(__name__)


def get_args() -> dict:
    parser = argparse.ArgumentParser()
    action = parser.add_subparsers(dest='action')
    scan = action.add_parser('scan')
    stream = action.add_parser('stream')
    group_verbosity = parser.add_mutually_exclusive_group()

    group_verbosity.add_argument(
        '-v',
        '--verbose',
        required=False,
        action='store_true',
        default=False,
        help='set log level to DEBUG'
    )

    group_verbosity.add_argument(
        '-q',
        '--quiet',
        required=False,
        action='store_true',
        default=False,
        help='set log level to CRITICAL'
    )

    scan.add_argument(
        '-t',
        '--timeout',
        required=False,
        default=5000,
        type=int,
        help='timeout for scanning local subnet for devices'
    )

    stream.add_argument(
        '-d',
        '--deviceuid',
        required=True,
        type=str,
        help='device UID to stream video from'
    )
    
    stream.add_argument(
        '-f',
        '--filename',
        required=True,
        type=argparse.FileType(mode='wb', bufsize=0),
        help='file to write video frames to; use - for stdout'
    )
    
    return parser.parse_args()


def init_logging(log_level: int) -> None:
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s [%(levelname)s] [%(name)s.%(funcName)s]: '
        '%(message)s'
    )


if __name__ == "__main__":
    args: dict = get_args()
    
    # configure log levels
    init_logging(
        10 if args.verbose 
        else 50 if args.quiet 
        else 20
    )

    # initialise the camera proxy
    proxy.initialise()

    if args.action == 'scan':
        devices: list[TutkDevice] = proxy.scan_local_subnet(timeout=\
                                                            args.timeout)
        