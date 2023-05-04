#!/usr/bin/env python3

"""
Example of using the tutk_proxy package to perform scanning and streaming 
using the underlying tutk_wrapper package.

Actions supported:
    - scan: scans local subnet for compatible devices using multicast packet
    - sync: syncs the local time with a remote device
    - stream: streams raw video frames from a remote device to target file
"""

from tutk_proxy import proxy
from typing import BinaryIO
import argparse
import logging
from tutk_proxy.models import (
    TutkDevice,
    TutkDeviceSettings
)

log = logging.getLogger(__name__)


def get_args() -> dict:
    parser = argparse.ArgumentParser()
    action = parser.add_subparsers(dest='action')
    action.required = True
    scan = action.add_parser('scan')
    stream = action.add_parser('stream')
    sync = action.add_parser('sync')
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
        help='device UID'
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
        type=argparse.FileType(mode='ab', bufsize=0),
        help='file to write video frames to; use - for stdout'
    )

    sync.add_argument(
        '-d',
        '--deviceuid',
        required=True,
        type=str,
        help='device UID'
    )

    sync.add_argument(
        '-u',
        '--username',
        required=True,
        type=str,
        help='username to use to connect to device'
    )

    sync.add_argument(
        '-p',
        '--password',
        required=True,
        type=str,
        help='password to use to connect to device'
    )

    sync.add_argument(
        '-t',
        '--timeout',
        required=False,
        default=5000,
        type=int,
        help='timeout for scanning and connecting to devices'
    )
    
    return parser.parse_args()


def init_logging(log_level: int) -> None:
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s [%(levelname)s] [%(name)s.%(funcName)s]: '
        '%(message)s'
    )


def find_device(
    devices: list[TutkDevice],
    uid: str
) -> TutkDevice:
    log.info(f'trying to find device with uid={uid}')
    matches = [d for d in devices if d.uid == uid]

    return next(iter(matches), None)


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

    target_device = find_device(
        devices=devices,
        uid=uid
    )

    if not target_device:
        log.fatal(f'unable to find device with uid={uid}')
        return
    
    log.info(f'found device with uid={uid}')

    target_device.device_settings = TutkDeviceSettings(
        username=username,
        password=password,
        timeout_s=int(timeout_ms / 1000)
    )
    
    target_device.connect()

    target_device.stream_to(
        dest_file=dest_file,
        blocking=True
    )


def action_sync(
    uid: str,
    username: str,
    password: str,
    timeout_ms: int
) -> None:
    devices: list[TutkDevice] = proxy.scan_local_subnet(timeout_ms=timeout_ms)

    target_device = find_device(
        devices=devices,
        uid=uid
    )

    if not target_device:
        log.fatal(f'unable to find device with uid={uid}')
        return
    
    log.info(f'found device with uid={uid}')

    target_device.device_settings = TutkDeviceSettings(
        username=username,
        password=password,
        timeout_s=int(timeout_ms / 1000)
    )

    target_device.connect()
    target_device.sync_time()


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

    log.info(f'args: {args}')

    if args.action == 'sync':
        action_sync(
            uid=args.deviceuid,
            username=args.username,
            password=args.password,
            timeout_ms=args.timeout
        )

    if args.action == 'scan':
        action_scan(timeout_ms=args.timeout)

    elif args.action == 'stream':
        action_stream(
            uid=args.deviceuid,
            username=args.username,
            password=args.password,
            timeout_ms=args.timeout,
            dest_file=args.filename
        )
