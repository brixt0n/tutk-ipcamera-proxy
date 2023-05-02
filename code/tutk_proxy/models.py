from dataclasses import dataclass
import tutk_wrapper.wrapper as tw
import tutk_wrapper.models as tm
import tutk_wrapper.exceptions as te
import tutk_wrapper.constants as tc
import ctypes as c
from utils.annotations import log_args
from .constants import IOTCSessionMode
from typing import BinaryIO
import logging


@dataclass
class TutkDeviceSettings():
    username: str = None
    password: str = None
    timeout_s: int = 5


@dataclass
class TutkDeviceState():
    client_sid: int = None
    device_sid: int = None
    channel_id: int = None
    session_mode: IOTCSessionMode = None
    packets_tx: int = 0
    packets_rx: int = 0
    resend_on: bool = False
    streaming: bool = False


class TutkDevice():
    @log_args
    def __init__(
        self,
        uid: str = None,
        ip_address: str = None,
        port: int = 0,
        friendly_name: str = '',
        device_settings: TutkDeviceSettings = None
    ) -> None:
        self.log = logging.getLogger(self.__class__.__name__)
        self.uid = uid
        self.ip_address = ip_address
        self.port = port
        self.friendly_name = friendly_name
        self.device_settings = device_settings
        self.device_state: TutkDeviceState = TutkDeviceState()
    
    @log_args
    def _reset_state(self) -> None:
        self.device_state = TutkDeviceState()

    @log_args
    def disconnect(self):
        """
        Disconnects from a device and frees device-side Session (SID).
        """
        raise NotImplementedError()

    @log_args
    def check_session(self) -> bool:
        """
        Checks device SID is active.
        """
        self.log.info(f'checking session')
        ses_info: tm.st_SInfo = tm.st_SInfo()

        try:
            tw.IOTC_Session_Check(
                self.device_state.device_sid,
                ses_info
            )
        except te.TutkLibraryException as e:
            self._reset_state()
            self.log.warn(f'got tutk library exception: {e}')
            return False
        
        self.log.info(f'session is valid')

        self.device_state.session_mode = IOTCSessionMode(ses_info.Mode)
        self.device_state.packets_rx = ses_info.RX_Packetcount
        self.device_state.packets_tx = ses_info.TX_Packetcount

        self.log.info(f'current device_state={self.device_state}')

        return True

    @log_args
    def connect(self) -> bool:
        """
        Connects to a device and gets a client- and device-side session (SID).
        """
        self.log.info(
            f'attempting to connect device '
            f'uid={self.uid}, '
            f'ip_address={self.ip_address}, '
            f'friendly_name={self.friendly_name}'
        )

        try:
            # get a client-side session
            self.log.debug(f'getting client-side session')
            client_sid: int = tw.IOTC_Get_SessionID()
            self.log.debug(
                f'got client-side session, '
                f'client_sid={str(client_sid)}'
            )

            # get a device-side session
            self.log.debug(f'getting device-side session')
            device_sid: int = tw.IOTC_Connect_ByUID_Parallel(
                self.uid.encode(),
                client_sid
            )
            self.log.debug(
                f'got device-side session, '
                f'device_sid={str(device_sid)}'
            )
        except te.TutkLibraryException as e:
            self.log.warn(f'got tutk library exception: {e}')
            return False
        
        self.device_state.client_sid = client_sid
        self.device_state.device_sid = device_sid
        self.log.info(
            f'connected to device, uid={self.uid}, '
            f'device_sid={str(device_sid)}'
        )
        return True


    @log_args
    def stream_to(
        self,
        dest_file: BinaryIO,
        blocking: bool = True
    ) -> None:
        self.log.info('checking session validity')

        if not self.check_session():
            self.log.warn('unable to stream; no valid session')
            return
        
        self.log.info('session is valid')

        resend: c.c_int = c.c_int(0)
        self.log.info(f'attempting to start av client')

        try:
            channel_id: int = tw.avClientStart2(
                self.device_state.device_sid,
                self.device_settings.username.encode(),
                self.device_settings.password.encode(),
                self.device_settings.timeout_s,
                None,
                0,
                c.byref(resend)
            )
        except te.TutkLibraryException as e:
            self.log.warn(f'got tutk library exception: {e}')
            return

        self.device_state.channel_id = channel_id
        self.device_state.resend_on = resend == 1
        self.log.info(f'started av client, current state: {self.device_state}')

        buffer = (c.c_char * 8)()
        self.log.info(f'attempting to send ioctrlmsg to start video')

        try:
            tw.avSendIOCtrl(
                self.device_state.channel_id,
                tc.AvIOCtrlMsgType.IOTYPE_USER_IPCAM_START,
                buffer,
                8
            )
        except te.TutkLibraryException as e:
            self.log.warn(f'got tutk library exception: {e}')
            return
        
        self.log.info(f'sent ioctrlmsg to start video')
