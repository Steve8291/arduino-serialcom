"""
This module sets up a serial communication protocol.
Use it along with the SeriaCom.cpp and SerialCom.h Arduino library.
It will attempt to reconnect if device is unplugged and replugged.
Parameters:
    port - Port name. If 'arduino' then port auto-detected.
    baudrate - Default = 6900
"""

import serial
import serial.tools.list_ports
from threading import Thread

__all__ = ['SerialCom', 'get_arduino_port', 'list_ports']


class SerialCom:
    def __init__(self, port, baudrate=9600):
        self._SPECIAL_BYTE = 253
        self._START_MARKER = 254
        self._END_MARKER = 255
        self._conn_type = port
        self._device_info = None
        self._recv_buffer = []
        self._data_array = []

        if self._conn_type == 'arduino':
            com_port = None
            while com_port is None:
                com_port = get_arduino_port()
        else:
            com_port = port

        self._ser = serial.Serial(com_port, baudrate, timeout=0)
        self._set_device_info()
        self._thread = Thread(target=self._read_data, daemon=True)
        self._thread.start()

    def __str__(self):
        return str(self._ser.get_settings())

    @property
    def device_info(self):
        """Return device info string. None if not connected.
        Can be used to check if connectivity was lost."""
        return self._device_info

    def _set_device_info(self):
        port_info = None
        ports = serial.tools.list_ports.comports()
        for port, desc, hwid in ports:
            if port == self._ser.port:
                port_info = f"Port: {port}  Baud: {self._ser.baudrate}  Desc: {desc} {hwid}"
                continue
        self._device_info = port_info

    def _reconnect(self):
        self._device_info = None
        com_port = None
        while com_port is None:
            if self._conn_type == 'arduino':
                com_port = get_arduino_port()
            else:
                ports = serial.tools.list_ports.comports()
                for port in ports:
                    if port.device == self._conn_type:
                        com_port = port.device
                        continue

        self._ser = serial.Serial(com_port, self._ser.baudrate, timeout=0)
        self._set_device_info()

    @property
    def recv_buffer(self):
        """Returns list of bytearray objects.
        bytearrays always iterate as ints"""
        return self._recv_buffer

    def _read_data(self):
        # Runs as a separate thread to keep collecting data.
        # Loops to continually read data from port.
        recv_tmp = bytearray()

        while True:
            recv_in_progress = False
            try:
                while (self._ser.in_waiting > 0):
                    read_byte = self._ser.read()  # Read one byte

                    if read_byte == self._START_MARKER.to_bytes(1, 'little'):
                        recv_tmp.clear()
                        recv_in_progress = True
                    elif read_byte == self._END_MARKER.to_bytes(1, 'little'):
                        # Copy recv_tmp list to _recv_buffer so it doesn't clear.
                        self._recv_buffer.append(recv_tmp.copy())
                        recv_tmp.clear()
                        recv_in_progress = False
                    elif read_byte == self._SPECIAL_BYTE.to_bytes(1, 'little') and recv_in_progress:
                        # Decode high bytes. Must be ints to perform arithmetic.
                        read_byte = int.from_bytes(self._ser.read(), 'little') + self._SPECIAL_BYTE
                        recv_tmp.append(read_byte)  # .append(int)
                    elif recv_in_progress:
                        recv_tmp.extend(read_byte)  # .extend(b'')
            except OSError:
                recv_tmp.clear()
                self._reconnect()

    def write_data(self, msg):
        """Accepts a bytearray, bytes, list, tuple, set, string, int"""
        if isinstance(msg, str):
            msg = bytes(msg, 'utf-8')
        elif isinstance(msg, int):
            msg = [msg]
        msg = bytearray(msg)
        message = bytearray()
        # Encode high bytes
        for byte in msg:
            if byte >= self._SPECIAL_BYTE:
                message.append(self._SPECIAL_BYTE)
                message.append(byte - self._SPECIAL_BYTE)
            else:
                message.append(byte)
        message.insert(0, self._START_MARKER)
        message.append(self._END_MARKER)
        try:
            self._ser.write(message)
        except OSError:
            self._reconnect()


def get_arduino_port():
    """
    Returns first port matching an Arduino UNO VID:PID
    If no ports located, returns: None
    """
    # https://github.com/arduino/ArduinoCore-avr/blob/63092126a406402022f943ac048fa195ed7e944b/boards.txt#L63-L72:
    board_id_list = [
        '2341:0043',
        '2341:0001',
        '2A03:0043',
        '2341:0243',
        '2341:006A'
    ]

    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in ports:
        if hwid[12:21] in board_id_list:
            return port


def list_ports():
    """ Returns a list of all active serial ports"""
    active_ports = []
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        if hwid != 'n/a':
            port_info = f"{port} {desc} {hwid}"
            active_ports.append(port_info)
    return active_ports
