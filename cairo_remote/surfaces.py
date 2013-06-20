import cairo
import struct
import zmq

from formats import *
from send import Sender as _Sender
 
class ImageSurface(_Sender):
    def __init__(self, format, width, height, socket):
        super(ImageSurface, self).__init__("ImageSurface", socket)
        self._format = format
        self._width = width
        self._height = height
        self._sock = socket
        # Send ID of this object
        self._send_iiii("__init__", id(self), format, width, height)

    @classmethod
    def create_for_data(self, data, format, width, height, stride = None):
        raise NotImplementedError()

    @classmethod
    def create_from_png(self, fObj):
        # TODO - Check type, support more file like objects as well as filenames
        send_s(self._sock, "create_from_png", fObj)

    @classmethod
    def format_stride_for_width(self, format, width):
        send_si(self._sock, "format_stride_for_width", format, width)

    def get_data(self):
        send(self._sock, "get_data")
        raise NotImplementedError()

    def get_format(self):
        return self._format

    def get_height(self):
        return self._height

    def get_stride(self):
        # Maybe we can get this during construction or fake it
        send(self._sock, "get_stride")
        raise NotImplementedError()

    def get_width():
        return self._width
    



