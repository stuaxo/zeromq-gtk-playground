import time
import zmq

from surfaces import ImageSurface
from context import Context

context = zmq.Context()
pub_sock = context.socket(zmq.PUB)
pub_sock.bind("ipc:///tmp/cairo-pushpub2")


im = ImageSurface(0, 200, 200, socket=pub_sock)
cr = Context( im, socket=pub_sock )
cr.rectangle(0, 0, 40, 40)
cr.fill()


while True:
    time.sleep(1)

