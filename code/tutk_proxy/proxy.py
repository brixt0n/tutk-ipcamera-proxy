from utils.annotations import log_args
import tutk_wrapper.wrapper as tw
import tutk_wrapper.exceptions as te
import tutk_wrapper.models as tm
import ctypes as c
from .models import (
    TutkDevice,
    TutkDeviceSettings,
    TutkDeviceState
)
import logging
from textwrap import dedent

log = logging.getLogger(__name__)

# connect to device by <device object>
# start recording <device> (to file)
# stop recording
# get single frame (png)
@log_args
def initialise(library_path: str='tutk_wrapper/lib/libIOTCAPIs_ALL.so') \
    -> None:
    """
    Initialise proxy dependencies e.g., tutk library, and prepare it to be 
    called.
    """
    log.info(f'attempting to load wrapper')
    try:
        tw.initialise(library_path)
    except te.TutkLibraryLoadException as e:
        log.fatal(e)
        raise e
    log.info(f'loaded wrapper')

    log.info(f'attempting to initialise IOTC library')
    try:
        tw.IOTC_Initialize2()
    except te.TutkLibraryLoadException as e:
        log.fatal(e)
        raise e
    log.info(f'initialised IOTC library')

    log.info(f'attempting to initialise av functions')
    try:
        tw.avInitialize()
    except te.TutkLibraryLoadException as e:
        log.fatal(e)
        raise e
    log.info(f'initialised av functions')


@log_args
def scan_local_subnet(
    timeout_ms: int=5000,
    max_devices_to_return: int=10
) -> list[TutkDevice]:
    """
    Scans the local subnet and returns a list of devices found.
    """
    log.info(f'attempting to scan local subnet for devices')
    device_array = (tm.st_LanSearchInfo2 * max_devices_to_return)()
    
    try:
        number_of_devices: int = tw.IOTC_Lan_Search2(
            device_array,
            max_devices_to_return,
            timeout_ms
        )
    except te.TutkLibraryException as e:
        log.fatal(f'got tutk library exception: {e}')
        exit(1)

    log.info(
        f'finished scanning local subnet, number_of_devices='
        f'{number_of_devices}'
    )

    device_array = device_array[:number_of_devices]
    device_list: list[TutkDevice] = list()

    # iterate over all devices and construct a TutkDevice object for each
    for s in device_array:
        uid = c.c_char_p(c.addressof(s.UID)).value.decode()
        ip = c.c_char_p(c.addressof(s.IP)).value.decode()
        name = c.c_char_p(c.addressof(s.DeviceName)).value.decode()
        port = int(s.port)

        log.info(
            f'device: '
            f'uid={uid}, '
            f'ip={ip}, '
            f'port={str(port)}, '
            f'name={name}'
        )

        d = TutkDevice(
            uid=uid,
            ip_address=ip,
            port=port,
            friendly_name=name
        )

        device_list.append(d)

    return device_list
