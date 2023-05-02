from enum import IntEnum


class IOTCErrorCode(IntEnum):
    IOTC_ER_NoERROR = 0
    IOTC_ER_SERVER_NOT_RESPONSE = -1
    IOTC_ER_FAIL_RESOLVE_HOSTNAME = -2
    IOTC_ER_ALREADY_INITIALIZED = -3
    IOTC_ER_FAIL_CREATE_MUTEX = -4
    IOTC_ER_FAIL_CREATE_THREAD = -5
    IOTC_ER_FAIL_CREATE_SOCKET = -6
    IOTC_ER_FAIL_SOCKET_OPT = -7
    IOTC_ER_FAIL_SOCKET_BIND = -8
    IOTC_ER_UNLICENSE = -10
    IOTC_ER_LOGIN_ALREADY_CALLED = -11
    IOTC_ER_NOT_INITIALIZED = -12
    IOTC_ER_TIMEOUT = -13
    IOTC_ER_INVALID_SID = -14
    IOTC_ER_UNKNOWN_DEVICE = -15
    IOTC_ER_FAIL_GET_LOCAL_IP = -16
    IOTC_ER_LISTEN_ALREADY_CALLED = -17
    IOTC_ER_EXCEED_MAX_SESSION = -18
    IOTC_ER_CAN_NOT_FIND_DEVICE = -19
    IOTC_ER_CONNECT_IS_CALLING = -20
    IOTC_ER_SESSION_CLOSE_BY_REMOTE = -22
    IOTC_ER_REMOTE_TIMEOUT_DISCONNECT = -23
    IOTC_ER_DEVICE_NOT_LISTENING = -24
    IOTC_ER_CH_NOT_ON = -26
    IOTC_ER_FAIL_CONNECT_SEARCH = -27
    IOTC_ER_MASTER_TOO_FEW = -28
    IOTC_ER_AES_CERTIFY_FAIL = -29
    IOTC_ER_SESSION_NO_FREE_CHANNEL = -31
    IOTC_ER_TCP_TRAVEL_FAILED = -32
    IOTC_ER_TCP_CONNECT_TO_SERVER_FAILED = -33
    IOTC_ER_CLIENT_NOT_SECURE_MODE = -34
    IOTC_ER_CLIENT_SECURE_MODE = -35
    IOTC_ER_DEVICE_NOT_SECURE_MODE = -36
    IOTC_ER_DEVICE_SECURE_MODE = -37
    IOTC_ER_INVALID_MODE = -38
    IOTC_ER_EXIT_LISTEN = -39
    IOTC_ER_NO_PERMISSION = -40
    IOTC_ER_NETWORK_UNREACHABLE = -41
    IOTC_ER_FAIL_SETUP_RELAY = -42
    IOTC_ER_NOT_SUPPORT_RELAY = -43
    IOTC_ER_NO_SERVER_LIST = -44
    IOTC_ER_DEVICE_MULTI_LOGIN = -45
    IOTC_ER_INVALID_ARG = -46
    IOTC_ER_NOT_SUPPORT_PE = -47
    IOTC_ER_DEVICE_EXCEED_MAX_SESSION = -48
    IOTC_ER_BLOCKED_CALL = -49
    IOTC_ER_SESSION_CLOSED = -50
    IOTC_ER_REMOTE_NOT_SUPPORTED = -51
    IOTC_ER_ABORTED = -52
    IOTC_ER_EXCEED_MAX_PACKET_SIZE = -53
    IOTC_ER_SERVER_NOT_SUPPORT = -54
    IOTC_ER_NO_PATH_TO_WRITE_DATA = -55
    IOTC_ER_SERVICE_IS_NOT_STARTED = -56
    IOTC_ER_STILL_IN_PROCESSING = -57
    IOTC_ER_NOT_ENOUGH_MEMORY = -58
    IOTC_ER_DEVICE_IS_BANNED = -59
    IOTC_ER_MASTER_NOT_RESPONSE = -60
    IOTC_ER_RESOURCE_ERROR = -61
    IOTC_ER_QUEUE_FULL = -62
    IOTC_ER_NOT_SUPPORT = -63
    IOTC_ER_DEVICE_IS_SLEEP = -64
    IOTC_ER_TCP_NOT_SUPPORT = -65
    IOTC_ER_WAKEUP_NOT_INITIALIZED = -66
    IOTC_ER_DEVICE_OFFLINE = -90
    IOTC_ER_MASTER_INVALID = -91


class AVErrorCode(IntEnum):
    AV_ER_NoERROR = 0
    AV_ER_INVALID_ARG = -20000
    AV_ER_BUFPARA_MAXSIZE_INSUFF = -20001
    AV_ER_EXCEED_MAX_CHANNEL = -20002
    AV_ER_MEM_INSUFF = -20003
    AV_ER_FAIL_CREATE_THREAD = -20004
    AV_ER_EXCEED_MAX_ALARM = -20005
    AV_ER_EXCEED_MAX_SIZE = -20006
    AV_ER_SERV_NO_RESPONSE = -20007
    AV_ER_CLIENT_NO_AVLOGIN = -20008
    AV_ER_WRONG_VIEWACCorPWD = -20009
    AV_ER_INVALID_SID = -20010
    AV_ER_TIMEOUT = -20011
    AV_ER_DATA_NOREADY = -20012
    AV_ER_INCOMPLETE_FRAME = -20013
    AV_ER_LOSED_THIS_FRAME = -20014
    AV_ER_SESSION_CLOSE_BY_REMOTE = -20015
    AV_ER_REMOTE_TIMEOUT_DISCONNECT = -20016
    AV_ER_SERVER_EXIT = -20017
    AV_ER_CLIENT_EXIT = -20018
    AV_ER_NOT_INITIALIZED = -20019
    AV_ER_CLIENT_NOT_SUPPORT = -20020
    AV_ER_SENDIOCTRL_ALREADY_CALLED = -20021
    AV_ER_SENDIOCTRL_EXIT = -20022
    AV_ER_NO_PERMISSION = -20023
    AV_ER_WRONG_ACCPWD_LENGTH = -20024
    AV_ER_IOTC_SESSION_CLOSED = -20025
    AV_ER_IOTC_DEINITIALIZED = -20026
    AV_ER_IOTC_CHANNEL_IN_USED = -20027
    AV_ER_WAIT_KEY_FRAME = -20028
    AV_ER_CLEANBUF_ALREADY_CALLED = -20029
    AV_ER_SOCKET_QUEUE_FULL = -20030
    AV_ER_ALREADY_INITIALIZED = -20031
    AV_ER_DASA_CLEAN_BUFFER = -20032


class AvIOCtrlMsgType(IntEnum):
    IOTYPE_USER_IPCAM_START = 0x01FF
    IOTYPE_USER_IPCAM_STOP = 0x02FF
    IOTYPE_USER_IPCAM_AUDIOSTART = 0x0300
    IOTYPE_USER_IPCAM_AUDIOSTOP = 0x0301

    IOTYPE_USER_IPCAM_SPEAKERSTART = 0x0350
    IOTYPE_USER_IPCAM_SPEAKERSTOP = 0x0351

    IOTYPE_USER_IPCAM_SETSTREAMCTRL_REQ = 0x0320
    IOTYPE_USER_IPCAM_SETSTREAMCTRL_RESP = 0x0321
    IOTYPE_USER_IPCAM_GETSTREAMCTRL_REQ = 0x0322
    IOTYPE_USER_IPCAM_GETSTREAMCTRL_RESP = 0x0323

    IOTYPE_USER_IPCAM_SETMOTIONDETECT_REQ = 0x0324
    IOTYPE_USER_IPCAM_SETMOTIONDETECT_RESP = 0x0325
    IOTYPE_USER_IPCAM_GETMOTIONDETECT_REQ = 0x0326
    IOTYPE_USER_IPCAM_GETMOTIONDETECT_RESP = 0x0327
    
    IOTYPE_USER_IPCAM_GETSUPPORTSTREAM_REQ = 0x0328 # Get Support Stream
    IOTYPE_USER_IPCAM_GETSUPPORTSTREAM_RESP = 0x0329 

    IOTYPE_USER_IPCAM_DEVINFO_REQ = 0x0330
    IOTYPE_USER_IPCAM_DEVINFO_RESP = 0x0331

    IOTYPE_USER_IPCAM_SETPASSWORD_REQ = 0x0332
    IOTYPE_USER_IPCAM_SETPASSWORD_RESP = 0x0333

    IOTYPE_USER_IPCAM_LISTWIFIAP_REQ = 0x0340
    IOTYPE_USER_IPCAM_LISTWIFIAP_RESP = 0x0341
    IOTYPE_USER_IPCAM_SETWIFI_REQ = 0x0342
    IOTYPE_USER_IPCAM_SETWIFI_RESP = 0x0343
    IOTYPE_USER_IPCAM_GETWIFI_REQ = 0x0344
    IOTYPE_USER_IPCAM_GETWIFI_RESP = 0x0345
    IOTYPE_USER_IPCAM_SETWIFI_REQ_2 = 0x0346
    IOTYPE_USER_IPCAM_GETWIFI_RESP_2 = 0x0347

    IOTYPE_USER_IPCAM_SETRECORD_REQ = 0x0310
    IOTYPE_USER_IPCAM_SETRECORD_RESP = 0x0311
    IOTYPE_USER_IPCAM_GETRECORD_REQ = 0x0312
    IOTYPE_USER_IPCAM_GETRECORD_RESP = 0x0313

    IOTYPE_USER_IPCAM_SETRCD_DURATION_REQ = 0x0314
    IOTYPE_USER_IPCAM_SETRCD_DURATION_RESP = 0x0315
    IOTYPE_USER_IPCAM_GETRCD_DURATION_REQ = 0x0316
    IOTYPE_USER_IPCAM_GETRCD_DURATION_RESP = 0x0317

    IOTYPE_USER_IPCAM_LISTEVENT_REQ = 0x0318
    IOTYPE_USER_IPCAM_LISTEVENT_RESP = 0x0319
    
    IOTYPE_USER_IPCAM_RECORD_PLAYCONTROL = 0x031A
    IOTYPE_USER_IPCAM_RECORD_PLAYCONTROL_RESP = 0x031B
    
    IOTYPE_USER_IPCAM_GETAUDIOOUTFORMAT_REQ = 0x032A
    IOTYPE_USER_IPCAM_GETAUDIOOUTFORMAT_RESP = 0x032B

    IOTYPE_USER_IPCAM_GET_EVENTCONFIG_REQ = 0x0400 # Get Event Config Msg Request
    IOTYPE_USER_IPCAM_GET_EVENTCONFIG_RESP = 0x0401 # Get Event Config Msg Response
    IOTYPE_USER_IPCAM_SET_EVENTCONFIG_REQ = 0x0402 # Set Event Config Msg req
    IOTYPE_USER_IPCAM_SET_EVENTCONFIG_RESP = 0x0403 # Set Event Config Msg resp

    IOTYPE_USER_IPCAM_SET_ENVIRONMENT_REQ = 0x0360
    IOTYPE_USER_IPCAM_SET_ENVIRONMENT_RESP = 0x0361
    IOTYPE_USER_IPCAM_GET_ENVIRONMENT_REQ = 0x0362
    IOTYPE_USER_IPCAM_GET_ENVIRONMENT_RESP = 0x0363
    
    IOTYPE_USER_IPCAM_SET_VIDEOMODE_REQ = 0x0370 # Set Video Flip Mode
    IOTYPE_USER_IPCAM_SET_VIDEOMODE_RESP = 0x0371
    IOTYPE_USER_IPCAM_GET_VIDEOMODE_REQ = 0x0372 # Get Video Flip Mode
    IOTYPE_USER_IPCAM_GET_VIDEOMODE_RESP = 0x0373
    
    IOTYPE_USER_IPCAM_FORMATEXTSTORAGE_REQ = 0x0380 # Format external storage
    IOTYPE_USER_IPCAM_FORMATEXTSTORAGE_RESP = 0x0381 #
    
    IOTYPE_USER_IPCAM_PTZ_COMMAND = 0x1001 # P2P PTZ Command Msg

    IOTYPE_USER_IPCAM_EVENT_REPORT = 0x1FFF # Device Event Report Msg
    IOTYPE_USER_IPCAM_RECEIVE_FIRST_IFRAME = 0x1002 # Send from client, used to talk to device that
                                                            # client had received the first I frame
    
    IOTYPE_USER_IPCAM_GET_FLOWINFO_REQ = 0x0390
    IOTYPE_USER_IPCAM_GET_FLOWINFO_RESP = 0x0391
    IOTYPE_USER_IPCAM_CURRENT_FLOWINFO = 0x0392
    
    IOTYPE_USER_IPCAM_GET_TIMEZONE_REQ = 0x3A0
    IOTYPE_USER_IPCAM_GET_TIMEZONE_RESP = 0x3A1
    IOTYPE_USER_IPCAM_SET_TIMEZONE_REQ = 0x3B0
    IOTYPE_USER_IPCAM_SET_TIMEZONE_RESP = 0x3B1
    

    IOTYPE_USER_IPCAM_GET_SAVE_DROPBOX_REQ = 0x500
    IOTYPE_USER_IPCAM_GET_SAVE_DROPBOX_RESP = 0x501
    IOTYPE_USER_IPCAM_SET_SAVE_DROPBOX_REQ = 0x502
    IOTYPE_USER_IPCAM_SET_SAVE_DROPBOX_RESP = 0x503