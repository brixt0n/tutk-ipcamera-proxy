#!/usr/bin/env python3

"""
Example of using the tutk_proxy package to perform scanning and streaming 
using the underlying tutk_wrapper package.
"""
from tutk_proxy import proxy
from typing import BinaryIO
import argparse
import logging
from tutk_proxy.models import (
    TutkDevice,
    TutkDeviceSettings,
    TutkDeviceState
)

log = logging.getLogger(__name__)


def get_args() -> dict:
    parser = argparse.ArgumentParser()
    action = parser.add_subparsers(dest='action')
    action.required = True
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
        help='timeout (ms) for scanning for / connecting to devices'
    )

    stream.add_argument(
        '-d',
        '--deviceuid',
        required=True,
        type=str,
        help='device UID to stream video from'
    )

    stream.add_argument(
        '-u',
        '--username',
        required=True,
        type=str,
        help='username to use to connect to device'
    )

    stream.add_argument(
        '-p',
        '--password',
        required=True,
        type=str,
        help='password to use to connect to device'
    )

    stream.add_argument(
        '-t',
        '--timeout',
        required=False,
        default=5000,
        type=int,
        help='timeout for scanning and connecting to devices'
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


def initialise(
    verbose: bool,
    quiet: bool
):
    # configure log levels
    init_logging(
        10 if verbose 
        else 50 if quiet 
        else 20
    )

    # initialise the camera proxy
    proxy.initialise()


def action_stream(
    uid: str,
    username: str,
    password: str,
    timeout_ms: int,
    dest_file: BinaryIO
) -> None:
    devices: list[TutkDevice] = proxy.scan_local_subnet(timeout_ms=timeout_ms)
    target_device: TutkDevice = None

    log.info(f'trying to find device with uid={uid}')
    for d in devices:
        if not d.uid == uid:
            continue

        log.info(f'found device with uid={uid}')
        target_device = d
        break

    if not target_device:
        log.fatal(f'unable to find device with uid={uid}')
        exit(1)

    d.device_settings = TutkDeviceSettings(
        username=username,
        password=password,
        timeout_s = int(timeout_ms / 1000)
    )

    d.connect()
    d.stream_to(
        dest_file,
        True
    )


def action_scan(timeout_ms: int = 5000) -> list[TutkDevice]:
    devices: list[TutkDevice] = proxy.scan_local_subnet(timeout_ms=timeout_ms)
        
    log.info(
        f'received '
        f'{str(len(devices))} device'
        f'{"" if len(devices)==1 else "s"}'
    )

    for d in devices:
        log.info(
            f'device: '
            f'uid={d.uid}, '
            f'ip={d.ip_address}, '
            f'port={str(d.port)}, '
            f'name={d.friendly_name}'
        )


if __name__ == "__main__":
    args: dict = get_args()
    
    initialise(
        args.verbose,
        args.quiet
    )

    if args.action == 'scan':
        action_scan(timeout=args.timeout)
    elif args.action == 'stream':
        action_stream(
            uid=args.deviceuid,
            username=args.username,
            password=args.password,
            timeout_ms=args.timeout,
            dest_file=args.filename
        )
