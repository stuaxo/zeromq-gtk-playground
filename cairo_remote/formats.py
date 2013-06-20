import cairo
import struct
import zmq


def create_sender(struct_format):
    """
    Create a send function for some struct_format

    :param struct_format: Struct format string for this command
    """
    def send_x(sock, cmd_type, cairo_cmd, *args):
        print 'send {} {}'.format(cmd_type, cairo_cmd)
        sock.send(cmd_type, zmq.SNDMORE)
        sock.send(cairo_cmd, zmq.SNDMORE)
        sock.send(struct_format.pack(*args))
    return send_x

def recv_reciever(struct_format):
    """
    Create a recv function for some struct_format

    :param struct_format: Struct format string for this command
    """
    def recv_x(sock):
        args = sock.recv(struct_format.unpack(sock.recv()))
        return args
    return recv_x


def send(sock, cmd_type, cairo_cmd):
    """
    Sender for commands that don't have any parameters
    """
    print 'send {} {}'.format(cmd_type, cairo_cmd)
    sock.send(cmd_type, zmq.SNDMORE)
    sock.send(cairo_cmd)



fmt_f = struct.Struct(format="<f")
fmt_ff = struct.Struct(format="<ff")
fmt_fff = struct.Struct(format="<fff")
fmt_ffff = struct.Struct(format="<ffff")
fmt_fffff = struct.Struct(format="<fffff")
fmt_ffffff = struct.Struct(format="<ffffff")


fmt_ii = struct.Struct(format="<ii")
fmt_iii = struct.Struct(format="<iii")
fmt_iiii = struct.Struct(format="<iiii")

fmt_s = struct.Struct(format="<s")
fmt_si = struct.Struct(format="<si")
fmt_sii = struct.Struct(format="<sii")
fmt_sis = struct.Struct(format="<sis")


send_f = create_sender(fmt_f)
send_ff = create_sender(fmt_ff)
send_fff = create_sender(fmt_fff)
send_ffff = create_sender(fmt_ffff)
send_fffff = create_sender(fmt_fffff)
send_ffffff = create_sender(fmt_ffffff)

send_ii = create_sender(fmt_ii)
send_iii = create_sender(fmt_iii)
send_iiii = create_sender(fmt_iiii)

send_s = create_sender(fmt_s)
send_si = create_sender(fmt_si)
send_sii = create_sender(fmt_sii)
send_sis = create_sender(fmt_sis)


