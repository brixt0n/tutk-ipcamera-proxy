from dataclasses import dataclass
import time
import datetime
import tutk_wrapper.wrapper as tw
import tutk_wrapper.models as tm
import tutk_wrapper.exceptions as te
import tutk_wrapper.constants as tc
import ctypes as c
from utils.annotations import log_args
from .constants import (
    IOTCSessionMode,
    StreamFormat,
    FRAME_BUFFER_SIZE,
    STREAM_LOG_INTERVAL
)
from typing import BinaryIO
import logging


@dataclass
class TutkDeviceSettings():
    username: str = None
    password: str = None
    timeout_s: int = 5


@dataclass
class TutkDeviceStreamInfo():
    frames_received: int = 0
    fps: int = 0
    last_frame_jpg: bytes = None
    last_frame_received_time: int = 0
    last_frame_size: int = 0
    dropped_frames: int = 0
    video_format: StreamFormat = StreamFormat.MEDIA_CODEC_UNKNOWN


@dataclass
class TutkDeviceState():
    client_sid: int = None
    device_sid: int = None
    channel_id_video: int = None
    channel_id_control: int = None
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
        self.stream_info: TutkDeviceStreamInfo = TutkDeviceStreamInfo()
    
    @log_args
    def _reset_state(self) -> None:
        self.device_state = TutkDeviceState()
    
    @log_args
    def _reset_stream_info(self) -> None:
        self.device_state.stream_info = TutkDeviceStreamInfo()

    @log_args
    def disconnect(self):
        """
        Disconnects from a device and frees device-side Session (SID).
        """
        raise NotImplementedError()

    @log_args
    def _check_session(self) -> bool:
        """
        Checks device SID is active.
        """
        self.log.info(f'checking session')

        if self.device_state.device_sid == None:
            self._reset_state()
            self.log.warn(f'session is not valid')
            return False

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
    def _send_ioctrl_msg(
        self,
        message_type: tc.AvIOCtrlMsgType,
        message_bytes: bytes
    ) -> bool:
        self.log.info(f'attempting to send ioctrlmsg')
        message_padded = message_bytes + bytes(8 - len(message_bytes))

        try:
            tw.avSendIOCtrl(
                self.device_state.channel_id_control,
                message_type,
                message_padded,
                8
            )
        except te.TutkLibraryException as e:
            self.log.warn(f'got tutk library exception: {e}')
            self._reset_state()
            return False
        
        self.log.info(f'sent ioctrlmsg')

        return True
    
    @log_args
    def _get_av_channel(self) -> int:
        """
        Gets an AV channel from the current device
        """
        self.log.info(f'attempting to get an av channel')
        resend = c.c_int()

        try:
            channel_id: int = tw.avClientStart2(
                self.device_state.device_sid,
                self.device_settings.username.encode(),
                self.device_settings.password.encode(),
                self.device_settings.timeout_s,
                None,
                0,
                resend
            )
        except te.TutkLibraryException as e:
            self.log.warn(f'got tutk library exception: {e}')
            self._reset_state()
            return

        self.device_state.resend_on = resend.value == 1
        self.log.info(f'got av channel: {str(channel_id)}')

        return channel_id

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
            client_sid = tw.IOTC_Get_SessionID()
            self.log.debug(
                f'got client-side session, '
                f'client_sid={str(client_sid)}'
            )

            # get a device-side session
            self.log.debug(f'getting device-side session')
            device_sid = tw.IOTC_Connect_ByUID_Parallel(
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
    def sync_time(self) -> None:
        self.log.info('checking session validity')

        if not self._check_session():
            self.log.warn('unable to stream; no valid session')
            return
        
        self.log.info('session is valid')
        self.log.info('attempting to get av channel')

        channel = self._get_av_channel()
        if channel == None:
            self.log.warn('unable to get av channel')
            return

        self.device_state.channel_id_control = channel
        self.log.info('got av channel')
        
        tz_diff = (
            datetime.datetime.now() 
            - datetime.datetime.utcnow()
        ).total_seconds()

        current_time_epoch = int(datetime.datetime.now().timestamp() + tz_diff)
        message_bytes = current_time_epoch.to_bytes(
                length=4,
                byteorder='little'
        )

        self.log.info(f'current timezone to gmt difference is {tz_diff}')
        self.log.info(f'attempting to send ioctrlmsg')
        
        success = self._send_ioctrl_msg(
            message_type=tc.AvIOCtrlMsgType.IOTYPE_USER_IPCAM_SET_TIME,
            message_bytes=message_bytes
        )

        if success:
            self.log.info(f'synced time')
        else:
            self.log.warn(f'error syncing time')
            return


    @log_args
    def stream_to(
        self,
        dest_file: BinaryIO,
        blocking: bool = True
    ) -> None:
        if self.device_state.streaming:
            self.log.warn('device already streaming')
            return
            
        self._reset_stream_info()
        self.device_state.streaming = True
        self.log.info('checking session validity')

        if not self._check_session():
            self.log.warn('unable to stream; no valid session')
            return
        
        self.log.info('session is valid')
        self.log.info('attempting to get av channel')

        channel = self._get_av_channel()
        if channel == None:
            self.log.warn('unable to get av channel')
            return

        self.device_state.channel_id_video = channel
        self.log.info('got av channel')
        
        self.log.info(f'attempting to send ioctrlmsg to start video')
        io_buffer = (c.c_char * 8)()

        try:
            tw.avSendIOCtrl(
                self.device_state.channel_id_video,
                tc.AvIOCtrlMsgType.IOTYPE_USER_IPCAM_START,
                io_buffer,
                8
            )
        except te.TutkLibraryException as e:
            self.log.warn(f'got tutk library exception: {e}')
            self._reset_state()
            return
        
        self.log.info(f'sent ioctrlmsg to start video')

        if blocking:
            self.log.info(f'attempting to start video streaming (blocking)')

            frame_buf = (c.c_char * FRAME_BUFFER_SIZE)()
            frame_buf_size_recvd = c.c_int()
            frame_buf_size_sent = c.c_int()
            frame_info = tm.FRAMEINFO()
            frame_info_size_recvd = c.c_int()
            frame_number = c.c_int()
            
            frame_count = 0
            fps_frames = 0
            fps_time = int(time.time())
            
            while True:
                try:
                    frame_data_size = tw.avRecvFrameData2(
                        self.device_state.channel_id_video,
                        frame_buf,
                        FRAME_BUFFER_SIZE,
                        frame_buf_size_recvd,
                        frame_buf_size_sent,
                        frame_info,
                        c.sizeof(tm.FRAMEINFO),
                        frame_info_size_recvd,
                        frame_number
                    )
                except te.TutkLibraryException as e:
                    self.log.debug(
                        f'got tutk library exception {e}'
                    )

                    # error codes we can probably safely ignore
                    if e.args[0] in (
                        tc.AVErrorCode.AV_ER_DATA_NOREADY,
                        tc.AVErrorCode.AV_ER_LOSED_THIS_FRAME,
                        tc.AVErrorCode.AV_ER_INCOMPLETE_FRAME
                    ):
                        time.sleep(0.01)
                        continue

                    # error codes we can't ignore
                    else:
                        self.log.warn(f'got tutk library exception: {e}')
                        self._reset_state()
                        break

                frame_count += 1
                cur_time = int(time.time())
                time_span = cur_time - fps_time
                dropped_frames = frame_count - frame_number.value

                self.stream_info.frames_received = frame_count
                self.stream_info.last_frame_received_time = cur_time
                self.stream_info.last_frame_size = frame_data_size
                self.stream_info.dropped_frames = dropped_frames
                self.stream_info.video_format = StreamFormat(frame_info.codec_id)

                dest_file.write(frame_buf[:frame_data_size])

                if cur_time != fps_time and not time_span % STREAM_LOG_INTERVAL:
                    fps = int((frame_count - fps_frames) / STREAM_LOG_INTERVAL)
                    self.stream_info.fps = fps
                    fps_frames = frame_count
                    fps_time = cur_time

                    self.log.info(f'status: {self.stream_info}')
            
            dest_file.close()
