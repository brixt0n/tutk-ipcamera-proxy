import logging
import ctypes as c
from utils.annotations import debug_log
from annotations import (
    requires_av_initialized,
    requires_tutk_library
)
from constants import (
    AVErrorCode,
    IOTCErrorCode
)
from exceptions import (
    TutkLibraryNotLoadedException,
    TutkAVLibraryNotInitializedException,
    TutkLibraryLoadException,
    TutkLibraryException
)
from models import (
    st_SInfo,
    st_LanSearchInfo2
)

logger = logging.getLogger(__name__)
library_instance: c.CDLL = None
av_initialized: bool = False


@debug_log
def initialise(library_path: str='tutk_wrapper/lib/libIOTCAPIs_ALL.so') \
    -> None:
    """
    Initialises the tutk library
    """
    try:
        library_instance = c.CDLL(library_path)
        logger.info(f'successfully loaded library at {library_path}')

    except OSError:
        raise TutkLibraryLoadException(f'failed to load library at \
                                       {library_path}')


@requires_tutk_library
@debug_log
def avInitialize(max_channel_num: c.c_int = 1) -> None:
    """
    This function is used by AV servers or AV clients to initialize AV
    module and shall be called before any AV module related function
    is invoked.
    """
    func = library_instance.avInitialize
    func.argtypes = [c.c_int]
    func.restype = AVErrorCode

    return_code = library_instance.avInitialize(max_channel_num)

    if return_code != AVErrorCode.AV_ER_NoERROR:
        raise TutkLibraryException(AVErrorCode(return_code).name)
    
    av_initialized = True


@requires_av_initialized
@requires_tutk_library
@debug_log
def avDeInitialize() -> None:
    """
    AV module shall be deinitialized before IOTC module is deinitialized.
    """
    func = library_instance.avDeInitialize
    func.argtypes = None
    func.restype = AVErrorCode

    return_code = library_instance.avDeInitialize()

    if return_code != AVErrorCode.AV_ER_NoERROR:
        raise TutkLibraryException(AVErrorCode(return_code).name)


@requires_av_initialized
@requires_tutk_library
@debug_log
def avClientStart2(
    session_id: c.c_int,
    device_account_name: c.POINTER(c.c_char),
    device_password: c.POINTER(c.c_char),
    timeout_s: c.c_ulong,
    service_type: c.POINTER(c.c_ulong),
    channel_id: c.c_uint8,
    resend_on: c.POINTER(c.c_int)
) -> c.c_int:
    """
    Start an AV re-send supported client by providing view account and 
    password. It shall pass the authentication of the AV server before 
    receiving AV data. Whether the re-send mechanism is enabled or not depends 
    on AV server settings and will set the result into pnResend parameter.
    """
    func = library_instance.avClientStart2
    func.argtypes = [
        c.c_int,
        c.POINTER(c.c_char),
        c.POINTER(c.c_char),
        c.c_ulong,
        c.POINTER(c.c_ulong),
        c.c_uint8,
        c.POINTER(c.c_int)
    ]
    func.restype = c.c_int

    return_code = library_instance.avClientStart2(
        session_id,
        device_account_name,
        device_password,
        timeout_s,
        service_type,
        channel_id,
        resend_on
    )

    if return_code < AVErrorCode.AV_ER_NoERROR:
        raise TutkLibraryException(AVErrorCode(return_code).name)
    
    return return_code


@requires_tutk_library
@debug_log
def IOTC_Connect_ByUID(device_uid: c.POINTER(c.c_char)) -> c.c_int:
    """
    A device or a client may use this function to check if the IOTC session
    is still alive as well as getting the IOTC session info.
    """
    func = library_instance.IOTC_Connect_ByUID
    func.argtypes = [c.POINTER(c.c_char)]
    func.restype = c.c_int

    return_code = library_instance.IOTC_Session_Check(device_uid)

    if return_code < IOTCErrorCode.IOTC_ER_NoERROR:
        raise TutkLibraryException(IOTCErrorCode(return_code).name)
    
    return return_code


@requires_tutk_library
@debug_log
def IOTC_Connect_ByUID_Parallel(
    device_uid: c.POINTER(c.c_char),
    session_id: c.c_int
) -> c.c_int:
    """
    This function is for a client to connect a device by specifying the UID of 
    that device, and bind to a free session ID from IOTC_Get_SessionID().
    If connection is established with the help of IOTC servers, the 
    #IOTC_ER_NoERROR will be returned in this function and then client can 
    communicate for the other later by using this IOTC session ID.
    If this function is called by multiple threads, the connections will be
    processed concurrently.
    """
    func = library_instance.IOTC_Connect_ByUID_Parallel
    func.argtypes = [
        c.POINTER(c.c_char),
        c.c_int
    ]
    func.restype = IOTCErrorCode

    return_code = library_instance.IOTC_Connect_ByUID_Parallel(
        device_uid,
        session_id
    )

    if return_code < IOTCErrorCode.IOTC_ER_NoERROR:
        raise TutkLibraryException(IOTCErrorCode(return_code).name)
    
    return return_code


@requires_tutk_library
@debug_log
def IOTC_Session_Check(
    session_id: c.c_int,
    session_info: c.POINTER(st_SInfo)
) -> c.c_int:
    """
    A device or a client may use this function to check if the IOTC session
    is still alive as well as getting the IOTC session info.
    """
    func = library_instance.IOTC_Session_Check
    func.argtypes = [ 
        c.c_int, 
        c.POINTER(st_SInfo)
    ]
    func.restype = IOTCErrorCode

    return_code = library_instance.IOTC_Session_Check(
        session_id,
        session_info
    )

    if return_code != IOTCErrorCode.IOTC_ER_NoERROR:
        raise TutkLibraryException(IOTCErrorCode(return_code).name)
    
    return return_code


@requires_tutk_library
@debug_log
def IOTC_Lan_Search2(
    search_info_array: c.POINTER(st_LanSearchInfo2),
    search_info_size: c.c_int,
    timeout_ms: c.c_int
) -> int:
    """
    When client and devices are in LAN, client can search devices and their 
    name by calling this function.
    """
    func = library_instance.IOTC_Lan_Search2
    func.argtypes = [
        c.POINTER(st_LanSearchInfo2),
        c.c_int,
        c.c_int
    ]
    func.restype = IOTCErrorCode

    return_code = library_instance.IOTC_Lan_Search2(
        search_info_array,
        search_info_size,
        timeout_ms
    )

    if return_code != IOTCErrorCode.IOTC_ER_NoERROR:
        raise TutkLibraryException(IOTCErrorCode(return_code).name)
    
    return return_code


@requires_tutk_library
@debug_log
def IOTC_Initialize2(udp_port: c.c_ushort = 0) -> int:
    """
    This function is used by devices or clients to initialize IOTC
    module and shall be called before	any IOTC module related
    function is invoked except for IOTC_Set_Max_Session_Number().
    """
    func = library_instance.IOTC_Initialize2
    func.argtypes = [c.c_ushort]
    func.restype = IOTCErrorCode

    return_code = library_instance.IOTC_Initialize2(udp_port)

    if return_code != IOTCErrorCode.IOTC_ER_NoERROR:
        raise TutkLibraryException(IOTCErrorCode(return_code).name)
    
    return return_code


@requires_tutk_library
@debug_log
def IOTC_DeInitialize() -> int:
    """
    IOTC_DeInitialize() will automatically close all IOTC sessions
    in local site while the remote site will find sessions have
    been closed after certain period of time. Therefore, it is
    suggested to close all sessions before invoking this function
    to ensure the remote site and real-time session status.
    """
    func = library_instance.IOTC_DeInitialize
    func.argtypes = None
    func.restype = IOTCErrorCode

    return_code = library_instance.IOTC_DeInitialize()

    if return_code != IOTCErrorCode.IOTC_ER_NoERROR:
        raise TutkLibraryException(IOTCErrorCode(return_code).name)
    
    return return_code


@requires_tutk_library
@debug_log
def IOTC_Session_Channel_ON(
    session_id: c.c_int,
    channel_id: c.c_uint8
) -> int:
    """
    A device or a client uses this function to turn on a IOTC channel
    before sending or receiving data through this IOTC channel.
    """
    func = library_instance.IOTC_Session_Channel_ON
    func.argtypes = [ 
        c.c_int,
        c.c_uint8
    ]
    func.restype = IOTCErrorCode

    return_code = library_instance.IOTC_Session_Channel_ON(
        session_id,
        channel_id
    )

    if return_code != IOTCErrorCode.IOTC_ER_NoERROR:
        raise TutkLibraryException(IOTCErrorCode(return_code).name)
    
    return return_code


@requires_tutk_library
@debug_log
def IOTC_Session_Get_Free_Channel(session_id: c.c_int) -> int:
    """
    A device or a client uses this function to get a free IOTC channel
    in a specified IOTC session. By default, IOTC channel of ID 0 is turned on
    once a IOTC session is established. If more IOTC channels are required
    by users, this function can always return a free IOTC channel until
    maximum IOTC channels are reached.
    """
    func = library_instance.IOTC_Session_Get_Free_Channel
    func.argtypes = [c.c_int]
    func.restype = IOTCErrorCode

    return_code = library_instance.IOTC_Session_Get_Free_Channel(session_id)

    if return_code < IOTCErrorCode.IOTC_ER_NoERROR:
        raise TutkLibraryException(IOTCErrorCode(return_code).name)
    
    return return_code


@requires_tutk_library
@debug_log
def IOTC_Session_Close(session_id: c.c_int) -> None:
    """
    Close a session.
    """
    func = library_instance.IOTC_Session_Close
    func.argtypes = [c.c_int]
    func.restype = IOTCErrorCode

    return_code = library_instance.IOTC_Session_Close(session_id)

    if return_code != IOTCErrorCode.IOTC_ER_NoERROR:
        raise TutkLibraryException(IOTCErrorCode(return_code).name)
