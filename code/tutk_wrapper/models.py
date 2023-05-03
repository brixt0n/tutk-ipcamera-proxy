import ctypes as c

class FRAMEINFO(c.Structure):
    """
    Metadata about a video frame received via avRecvFrameData2
    """
    
    """
    unsigned short codec_id;	// Media codec type defined in sys_mmdef.h,
								// MEDIA_CODEC_AUDIO_PCMLE16 for audio,
								// MEDIA_CODEC_VIDEO_H264 for video.
	unsigned char flags;		// Combined with IPC_FRAME_xxx.
	unsigned char cam_index;	// 0 - n
	unsigned char onlineNum;	// number of client connected this device
	unsigned char reserve1[3];
	unsigned int reserve2;	//
	unsigned int timestamp;	// Timestamp of the frame, in milliseconds
    """
    _fields_ = [
        ("codec_id", c.c_ushort),
        ("flags", c.c_ubyte),
        ("cam_index", c.c_ubyte),
        ("onlineNum", c.c_ubyte),
        ("reserve1", c.c_ubyte * 3),
        ("reserve2", c.c_uint),
        ("timestamp", c.c_uint)
    ]


class st_SInfo(c.Structure):
    """
    IOTC session info, containing all the information when a IOTC session is
    established between a device and a client. Users can use 
    IOTC_Session_Check() to get IOTC session information.
    """

    """
    unsigned char Mode; //!< 0: P2P mode, 1: Relay mode, 2: LAN mode
    char CorD; //!< 0: As a Client, 1: As a Device
    char UID[21]; //!< The UID of the device
    char RemoteIP[17]; //!< The IP address of remote site used during this 
        IOTC session
    unsigned short RemotePort; //!< The port number of remote site used during 
        this IOTC session
    unsigned long TX_Packetcount; //!< The total packets sent from the device 
        and the client during this IOTC session
    unsigned long RX_Packetcount; //!< The total packets received in the 
        device and the client during this IOTC session
    unsigned long IOTCVersion; //!< The IOTC version
    unsigned short VID; //!< The Vendor ID, part of VPG mechanism
    unsigned short PID; //!< The Product ID, part of VPG mechanism
    unsigned short GID; //!< The Group ID, part of VPG mechanism
    unsigned char NatType; //!< The remote NAT type
    unsigned char isSecure; //!< 0: The IOTC session is in non-secure mode, 1: 
        The IOTC session is in secure mode
    """
    #_pack_ = 1
    _fields_ = [
        ("Mode", c.c_ubyte),
        ("CorD", c.c_byte),
        ("UID", c.c_byte * 21),
        ("RemoteIP", c.c_byte * 17),
        ("RemotePort", c.c_ushort),
        ("TX_Packetcount", c.c_ulong),
        ("RX_Packetcount", c.c_ulong),
        ("IOTCVersion", c.c_ulong),
        ("VID", c.c_ushort),
        ("PID", c.c_ushort),
        ("GID", c.c_ushort),
        ("NatType", c.c_ubyte),
        ("isSecure", c.c_ubyte)
    ]


class st_LanSearchInfo2(c.Structure):
    """
    Device serch info, containing all the information and device name
    when client searches devices in LAN.
    """

    """
    char UID[21]; //!< The UID of discoveried device
    char IP[16]; //!< The IP address of discoveried device
    unsigned short port; //!< The port number of discoveried device used for 
        IOTC session connection
    char DeviceName[129]; //!< The Name of discoveried device
    char Reserved; //!< Reserved, no use
    """
    #_pack_ = 1
    _fields_ = [
        ("UID", c.c_byte * 21),
        ("IP", c.c_byte * 16),
        ("port", c.c_ushort),
        ("DeviceName", c.c_byte * 129),
        ("Reserved", c.c_byte)
    ]
