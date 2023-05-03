import logging
import ctypes as c
from utils.annotations import log_args
from .annotations import (
    requires_av_initialized,
    requires_tutk_library
)
from .constants import (
    AVErrorCode,
    IOTCErrorCode,
    AvIOCtrlMsgType
)
from .exceptions import (
    TutkLibraryNotLoadedException,
    TutkAVLibraryNotInitializedException,
    TutkLibraryLoadException,
    TutkLibraryException
)
from .models import (
    st_SInfo,
    st_LanSearchInfo2,
    FRAMEINFO
)
import tutk_wrapper.shared as shared

logger = logging.getLogger(__name__)


@log_args
def initialise(library_path: str='tutk_wrapper/lib/libIOTCAPIs_ALL.so') \
    -> None:
    """
    Initialises the tutk library
    """

    try:
        shared.library_instance = c.CDLL(library_path)
        logger.info(f'successfully loaded library at {library_path}')

    except OSError:
        raise TutkLibraryLoadException(f'failed to load library at \
                                       {library_path}')


@requires_tutk_library
@log_args
def avInitialize(max_channel_num: c.c_int = 1) -> None:
    """
    This function is used by AV servers or AV clients to initialize AV
    module and shall be called before any AV module related function
    is invoked.
    """
    func = shared.library_instance.avInitialize
    func.argtypes = (c.c_int,)
    func.restype = c.c_int

    rc = shared.library_instance.avInitialize(max_channel_num)

    if rc < AVErrorCode.AV_ER_NoERROR:
        raise TutkLibraryException(AVErrorCode(rc))
    
    shared.av_initialized = True


@requires_av_initialized
@requires_tutk_library
@log_args
def avDeInitialize() -> None:
    """
    AV module shall be deinitialized before IOTC module is deinitialized.
    """
    func = shared.library_instance.avDeInitialize
    func.argtypes = None
    func.restype = c.c_int

    rc = shared.library_instance.avDeInitialize()

    if rc != AVErrorCode.AV_ER_NoERROR:
        raise TutkLibraryException(AVErrorCode(rc))


@requires_av_initialized
@requires_tutk_library
@log_args
def avClientCleanBuf(channel_id: c.c_int = 1) -> None:
    """
    A client with multiple device connection application should call
    this function to clean AV buffer while switch to another devices.
    """
    func = shared.library_instance.avClientCleanBuf
    func.argtypes = (c.c_int,)
    func.restype = c.c_int

    rc = shared.library_instance.avClientCleanBuf(channel_id)

    if rc != AVErrorCode.AV_ER_NoERROR:
        raise TutkLibraryException(AVErrorCode(rc))


@requires_av_initialized
@requires_tutk_library
@log_args
def avRecvFrameData2(
    channel_id: c.c_int,
    frame_data_buffer: c.POINTER(c.c_char),
    frame_data_buffer_size: c.c_int,
    frame_data_size_received: c.POINTER(c.c_int),
    frame_data_size_sent: c.POINTER(c.c_int),
    frame_info: c.POINTER(FRAMEINFO),
    frame_info_size: c.c_int,
    frame_info_size_received: c.POINTER(c.c_int),
    frame_number: c.POINTER(c.c_int)
) -> c.c_int:
    """
    This function is used by AV servers or AV clients to send a AV IO control.
    """
    func = shared.library_instance.avRecvFrameData2
    func.argtypes = (
        c.c_int,
        c.POINTER(c.c_char),
        c.c_int,
        c.POINTER(c.c_int),
        c.POINTER(c.c_int),
        c.POINTER(FRAMEINFO),
        c.c_int,
        c.POINTER(c.c_int),
        c.POINTER(c.c_int)
    )
    func.restype = c.c_int

    rc = shared.library_instance.avRecvFrameData2(
        channel_id,
        frame_data_buffer,
        frame_data_buffer_size,
        frame_data_size_received,
        frame_data_size_sent,
        frame_info,
        frame_info_size,
        frame_info_size_received,
        frame_number
    )

    if rc < AVErrorCode.AV_ER_NoERROR:
        raise TutkLibraryException(AVErrorCode(rc))
    
    return rc


@requires_av_initialized
@requires_tutk_library
@log_args
def avSendIOCtrl(
    channel_id: c.c_int,
    io_ctrl_type: c.c_uint,
    io_ctrl_buffer: c.POINTER(c.c_char),
    io_ctrl_buffer_size: c.c_int
) -> None:
    """
    This function is used by AV servers or AV clients to send a AV IO control.
    """
    func = shared.library_instance.avSendIOCtrl
    func.argtypes = (
        c.c_int,
        c.c_uint,
        c.POINTER(c.c_char),
        c.c_int
    )
    func.restype = c.c_int

    rc = shared.library_instance.avSendIOCtrl(
        channel_id,
        io_ctrl_type,
        io_ctrl_buffer,
        io_ctrl_buffer_size
    )

    if rc != AVErrorCode.AV_ER_NoERROR:
        raise TutkLibraryException(AVErrorCode(rc))
    
    return rc


@requires_av_initialized
@requires_tutk_library
@log_args
def avClientStart2(
    session_id: c.c_int,
    device_account_name: c.POINTER(c.c_char),
    device_password: c.POINTER(c.c_char),
    timeout_s: c.c_ulong,
    service_type: c.POINTER(c.c_ulong),
    channel_id: c.c_ubyte,
    resend_on: c.POINTER(c.c_int)
) -> c.c_int:
    """
    Start an AV re-send supported client by providing view account and 
    password. It shall pass the authentication of the AV server before 
    receiving AV data. Whether the re-send mechanism is enabled or not depends 
    on AV server settings and will set the result into pnResend parameter.
    """
    func = shared.library_instance.avClientStart2
    func.argtypes = (
        c.c_int,
        c.POINTER(c.c_char),
        c.POINTER(c.c_char),
        c.c_ulong,
        c.POINTER(c.c_ulong),
        c.c_ubyte,
        c.POINTER(c.c_int)
    )
    func.restype = c.c_int

    rc = shared.library_instance.avClientStart2(
        session_id,
        device_account_name,
        device_password,
        timeout_s,
        service_type,
        channel_id,
        resend_on
    )

    if rc < AVErrorCode.AV_ER_NoERROR:
        raise TutkLibraryException(AVErrorCode(rc).name)
    
    return rc


@requires_tutk_library
@log_args
def IOTC_Connect_ByUID(device_uid: c.POINTER(c.c_char)) -> c.c_int:
    """
    A device or a client may use this function to check if the IOTC session
    is still alive as well as getting the IOTC session info.
    """
    func = shared.library_instance.IOTC_Connect_ByUID
    func.argtypes = (c.POINTER(c.c_char),)
    func.restype = c.c_int

    rc = shared.library_instance.IOTC_Connect_ByUID(device_uid)

    if rc < IOTCErrorCode.IOTC_ER_NoERROR:
        raise TutkLibraryException(IOTCErrorCode(rc).name)
    
    return rc


@requires_tutk_library
@log_args
def IOTC_Get_SessionID() -> c.c_int:
    """
    This function is for a client to get a free session ID used for a 
    parameter of IOTC_Connect_ByUID_Parallel().
    """
    func = shared.library_instance.IOTC_Get_SessionID
    func.argtypes = None
    func.restype = c.c_int

    rc = shared.library_instance.IOTC_Get_SessionID()

    if rc < IOTCErrorCode.IOTC_ER_NoERROR:
        raise TutkLibraryException(IOTCErrorCode(rc).name)
    
    return rc


@requires_tutk_library
@log_args
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
    func = shared.library_instance.IOTC_Connect_ByUID_Parallel
    func.argtypes = (
        c.POINTER(c.c_char),
        c.c_int
    )
    func.restype = c.c_int

    rc = shared.library_instance.IOTC_Connect_ByUID_Parallel(
        device_uid,
        session_id
    )

    if rc < IOTCErrorCode.IOTC_ER_NoERROR:
        raise TutkLibraryException(IOTCErrorCode(rc).name)
    
    return rc


@requires_tutk_library
@log_args
def IOTC_Session_Check(
    session_id: c.c_int,
    session_info: c.POINTER(st_SInfo)
) -> None:
    """
    A device or a client may use this function to check if the IOTC session
    is still alive as well as getting the IOTC session info.
    """
    func = shared.library_instance.IOTC_Session_Check
    func.argtypes = ( 
        c.c_int, 
        c.POINTER(st_SInfo)
    )
    func.restype = c.c_int

    rc = shared.library_instance.IOTC_Session_Check(
        session_id,
        session_info
    )

    if rc != IOTCErrorCode.IOTC_ER_NoERROR:
        raise TutkLibraryException(IOTCErrorCode(rc).name)


@requires_tutk_library
@log_args
def IOTC_Lan_Search2(
    search_info_array: c.POINTER(st_LanSearchInfo2),
    search_info_size: c.c_int,
    timeout_ms: c.c_int
) -> c.c_int:
    """
    When client and devices are in LAN, client can search devices and their 
    name by calling this function.
    """
    func = shared.library_instance.IOTC_Lan_Search2
    func.argtypes = (
        c.POINTER(st_LanSearchInfo2),
        c.c_int,
        c.c_int
    )
    func.restype = c.c_int

    rc = shared.library_instance.IOTC_Lan_Search2(
        search_info_array,
        search_info_size,
        timeout_ms
    )

    if rc < IOTCErrorCode.IOTC_ER_NoERROR:
        raise TutkLibraryException(IOTCErrorCode(rc).name)

    return rc


@requires_tutk_library
@log_args
def IOTC_Initialize2(udp_port: c.c_ushort = 0) -> c.c_int:
    """
    This function is used by devices or clients to initialize IOTC
    module and shall be called before any IOTC module related
    function is invoked except for IOTC_Set_Max_Session_Number().
    """
    func = shared.library_instance.IOTC_Initialize2
    func.argtypes = (c.c_ushort,)
    func.restype = c.c_int

    rc = shared.library_instance.IOTC_Initialize2(udp_port)

    if rc != IOTCErrorCode.IOTC_ER_NoERROR:
        raise TutkLibraryException(IOTCErrorCode(rc).name)
    
    return rc


@requires_tutk_library
@log_args
def IOTC_DeInitialize() -> c.c_int:
    """
    IOTC_DeInitialize() will automatically close all IOTC sessions
    in local site while the remote site will find sessions have
    been closed after certain period of time. Therefore, it is
    suggested to close all sessions before invoking this function
    to ensure the remote site and real-time session status.
    """
    func = shared.library_instance.IOTC_DeInitialize
    func.argtypes = None
    func.restype = c.c_int

    rc = shared.library_instance.IOTC_DeInitialize()

    if rc != IOTCErrorCode.IOTC_ER_NoERROR:
        raise TutkLibraryException(IOTCErrorCode(rc).name)
    
    return rc


@requires_tutk_library
@log_args
def IOTC_Session_Channel_ON(
    session_id: c.c_int,
    channel_id: c.c_ubyte
) -> c.c_int:
    """
    A device or a client uses this function to turn on a IOTC channel
    before sending or receiving data through this IOTC channel.
    """
    func = shared.library_instance.IOTC_Session_Channel_ON
    func.argtypes = (
        c.c_int,
        c.c_ubyte
    )
    func.restype = c.c_int

    rc = shared.library_instance.IOTC_Session_Channel_ON(
        session_id,
        channel_id
    )

    if rc != IOTCErrorCode.IOTC_ER_NoERROR:
        raise TutkLibraryException(IOTCErrorCode(rc).name)
    
    return rc


@requires_tutk_library
@log_args
def IOTC_Session_Get_Free_Channel(session_id: c.c_int) -> c.c_int:
    """
    A device or a client uses this function to get a free IOTC channel
    in a specified IOTC session. By default, IOTC channel of ID 0 is turned on
    once a IOTC session is established. If more IOTC channels are required
    by users, this function can always return a free IOTC channel until
    maximum IOTC channels are reached.
    """
    func = shared.library_instance.IOTC_Session_Get_Free_Channel
    func.argtypes = (c.c_int,)
    func.restype = c.c_int

    rc = \
        shared.library_instance.IOTC_Session_Get_Free_Channel(session_id)

    if rc < IOTCErrorCode.IOTC_ER_NoERROR:
        raise TutkLibraryException(IOTCErrorCode(rc).name)
    
    return rc


@requires_tutk_library
@log_args
def IOTC_Session_Close(session_id: c.c_int) -> None:
    """
    Close a session.
    """
    func = shared.library_instance.IOTC_Session_Close
    func.argtypes = (c.c_int,)
    func.restype = c.c_int

    rc = \
        shared.library_instance.IOTC_Session_Close(session_id)

    if rc != IOTCErrorCode.IOTC_ER_NoERROR:
        raise TutkLibraryException(IOTCErrorCode(rc).name)
