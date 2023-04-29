from dataclasses import dataclass
from tutk_wrapper import wrapper
from utils.annotations import log_args
from .constants import IOTCSessionMode
import logging


@dataclass
class TutkDeviceSettings():
    username: str = None
    password: str = None
    connect_timeout_seconds: int = 10


@dataclass
class TutkDeviceState():
    connected: bool = False
    session_id: int = None
    channel_id: int = None
    session_mode: IOTCSessionMode = None
    resend_on: bool = False


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
    def connect():
        raise NotImplementedError()
    
    @log_args
    def disconnect():
        raise NotImplementedError()
    
    
    