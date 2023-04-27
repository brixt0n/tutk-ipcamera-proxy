from dataclasses import dataclass
from tutk_wrapper import wrapper
from utils.annotations import debug_log
from constants import IOTCSessionMode
import logging


@dataclass
class TutkDeviceSettings():
    username: str = None
    password: str = None
    connect_timeout_seconds: int = 10


@dataclass
class TutkDeviceState():
    connected: bool = False
    ip_address: str = None
    session_id: int = None
    channel_id: int = None
    session_mode: IOTCSessionMode = None
    resend_on: bool = False


class TutkDevice():
    @debug_log
    def __init__(
        self,
        friendly_name: str,
        uid: str = None,
        device_settings: TutkDeviceSettings = None
    ):
        self.log = logging.getLogger(self.__class__.__name__)
        self.friendly_name: str = friendly_name
        self.uid: str = uid
        self.device_settings: TutkDeviceSettings = device_settings
        self.device_state: TutkDeviceState = TutkDeviceState()

    @debug_log
    def connect():
        raise NotImplementedError()
    
    @debug_log
    def discconnect():
        raise NotImplementedError()
    
    
    