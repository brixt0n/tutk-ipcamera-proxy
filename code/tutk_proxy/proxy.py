from ctypes import CDLL
from utils.annotations import debug_log
import tutk_wrapper.wrapper as tw
import tutk_wrapper.exceptions as te
from models import (
    TutkDevice,
    TutkDeviceSettings,
    TutkDeviceState
)
import logging

log = logging.getLogger(__name__)


# scan for devices on local subnet, return <device objects>
# connect to device by <device object>
# start recording <device> (to file)
# stop recording
# get single frame (png)
@debug_log
def initialise(library_path: str='./tutk/lib/libIOTCAPIs_ALL.so') -> None:
    """
    Initialises the tutk library.
    """
    log.info(f'attempting to initialise wrapper')

    try:
        tw.initialise(library_path)
        log.info(f'successfully initialised wrapper')

    except te.TutkLibraryLoadException as e:
        log.fatal(e)
        raise e


@debug_log
def scan_local_subnet() -> list[TutkDevice]:
    """
    Scans the local subnet and returns a list of devices found.
    """
    log.info(f'attempting to scan local subnet for devices')

    try:
        

    except te.TutkLibraryNotLoadedException as e:
        log.fatal(e)
        raise e

    log.info(f'successfully initialised wrapper')

