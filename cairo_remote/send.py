from formats import send as _send
from formats import send_f as _send_f
from formats import send_ff as _send_ff
from formats import send_fff as _send_fff
from formats import send_ffff as _send_ffff
from formats import send_fffff as _send_fffff
from formats import send_ffffff as _send_ffffff


from formats import send_ii as _send_ii

from formats import send_iiii as _send_iiii

from formats import send_sii as _send_sii


class Sender(object):
    def __init__(self, cmd_type, sock):
        """
        :param send_type: Type of target, e.g. "Context"
        :parm sock: zeromq socket to send over
        """
        self._cmd_type = cmd_type
        self._sock = sock

    def _send(self, cmd):
        _send(self._sock, self._cmd_type, cmd)

    def _send_f(self, cmd, *args):
        _send_f(self._sock, self._cmd_type, cmd, *args)

    def _send_ff(self, cmd, *args):
        _send_ff(self._sock, self._cmd_type, cmd, *args)

    def _send_fff(self, cmd, *args):
        _send_fff(self._sock, self._cmd_type, cmd, *args)

    def _send_ffff(self, cmd, *args):
        _send_ffff(self._sock, self._cmd_type, cmd, *args)

    def _send_fffff(self, cmd, *args):
        _send_fffff(self._sock, self._cmd_type, cmd, *args)

    def _send_ffffff(self, cmd, *args):
        _send_ffffff(self._sock, self._cmd_type, cmd, *args)

    def _send_ii(self, cmd, *args):
        _send_ii(self._sock, self._cmd_type, cmd, *args)

    def _send_iiii(self, cmd, *args):
        _send_iiii(self._sock, self._cmd_type, cmd, *args)

    def _send_sii(self, cmd, *args):
        _send_sii(self._sock, self._cmd_type, cmd, *args)

