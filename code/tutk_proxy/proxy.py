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


# scan for devices on local subnet, return <device objects>
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

@log_args
def scan_local_subnet(
    timeout: int=2000,
    max_devices_to_return: int=5
) -> list[TutkDevice]:
    """
    Scans the local subnet and returns a list of devices found.
    """
    log.info(f'attempting to scan local subnet for devices')

    struct_size: int = c.sizeof(tm.st_LanSearchInfo2)
    log.debug(f'sizeof st_LanSearchInfo2={struct_size}')

    try:
        buffer: c.Array[c.c_char] = c.create_string_buffer(
            struct_size * max_devices_to_return
        )

        number_of_devices: int = tw.IOTC_Lan_Search2(
            buffer,
            c.c_int(max_devices_to_return),
            c.c_int(timeout)
        )
    except te.TutkLibraryNotLoadedException as e:
        log.fatal(e)
        raise e

    log.info(
        f'finished scanning local subnet, number_of_devices='
        f'{number_of_devices}'
    )

    device_list: list[TutkDevice] = list()
    cur_device: int = 0

    # iterate over all devices and construct a TutkDevice object for each
    while cur_device < number_of_devices:
        slice_start = cur_device * struct_size
        slice_end = slice_start + struct_size

        # create an instance of the native struct from the buffer
        s = tm.st_LanSearchInfo2.from_buffer_copy(buffer, slice_start)

        # extract and convert fields from native struct
        uid = c.c_char_p(c.addressof(s.UID)).value.decode()
        ip = c.c_char_p(c.addressof(s.IP)).value.decode()
        name = c.c_char_p(c.addressof(s.DeviceName)).value.decode()
        port = int(s.port)

        log.info(
            f'device {str(cur_device)}: '
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
        cur_device += 1

    return device_list
