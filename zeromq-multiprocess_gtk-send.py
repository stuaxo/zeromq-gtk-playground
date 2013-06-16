#!/usr/bin/python

'''
Drawing the same images to many windows using cairo
and zero mq.


Requirements:
pyzmq, gtk3


Extended from Jan Bodnars Zetcode PyCairo example and
Learn ZeroMQ by Example in Python by Jaume Devesa


ZetCode:
author: Jan Bodnar
website: zetcode.com 
last edited: August 2012
'''

import math
import multiprocessing
import time
import threading
import struct
import sys

from gi.repository import Gtk, Gdk
import Queue
import cairo
import zmq


def pub_function(context):
    """ Definition of the pub socket.

        It published messages in unidirectional way.
    """
    pub_sock = context.socket(zmq.PUB)
    pub_sock.bind("ipc:///tmp/cairo-pushpub")

    frame = 0
    while True:
        for i in range(0, 800):  # Used for positioning the squares
            frame += 1
            # ZeroMQ messages can be broken up into multiple parts.
            # Messages are guaranteed to either come with all parts or not at all,
            # so don't worry about only receiving a partial message.
            
            # We're going to send the cmd_type in a separate part, it's what the SUB socket
            # will use to decide if it wants to receive this message.
            # You don't need to use two parts for a pub/sub socket, but if you're using
            # cmd_types its a good idea as matching terminates after the first part.
            #print "Send draw commands"

            pub_sock.send('draw', zmq.SNDMORE)   #Command Type
            pub_sock.send('set_source_rgba', zmq.SNDMORE)               #Command
            pub_sock.send(struct.pack("<ffff", 1, 1, 0, 1))


            pub_sock.send('draw', zmq.SNDMORE)     #Command Type
            pub_sock.send('paint')   #Command Type

            pub_sock.send('draw', zmq.SNDMORE)   #Command Type
            pub_sock.send('set_source_rgb', zmq.SNDMORE)               #Command
            pub_sock.send(struct.pack("<fff", 0, 0, 0))

            pub_sock.send('draw', zmq.SNDMORE)     #Command Type
            pub_sock.send('save')          #Command

            for j in range(5, 15):

                pub_sock.send("draw", zmq.SNDMORE)
                pub_sock.send('rotate', zmq.SNDMORE)
                pub_sock.send(struct.pack("<f", 90 + j * 10 + (i / 100.0)))




                pub_sock.send("draw", zmq.SNDMORE)
                pub_sock.send('move_to', zmq.SNDMORE)
                pub_sock.send(struct.pack("<ff", 24, 24))


                pub_sock.send('draw', zmq.SNDMORE)   #Command Type
                pub_sock.send('set_source_rgb', zmq.SNDMORE)               #Command
                pub_sock.send(struct.pack("<fff", math.sin(i / 10.0), math.cos(i / 15.0), math.sin(i / 25.0 + j / 100.0)))

                pub_sock.send('draw', zmq.SNDMORE)     #Command Type
                pub_sock.send('rectangle', zmq.SNDMORE)          #Command
                pub_sock.send(struct.pack("<ffff", i, i / 4.0, 40 + j * 3, 40 + j * 3))


                pub_sock.send('draw', zmq.SNDMORE)     #Command Type
                pub_sock.send('fill')          #Command




                pub_sock.send('draw', zmq.SNDMORE)   #Command Type
                pub_sock.send('set_source_rgb', zmq.SNDMORE)               #Command
                pub_sock.send(struct.pack("<fff", 1, 0, 0))

                pub_sock.send('draw', zmq.SNDMORE)     #Command Type
                pub_sock.send('rectangle', zmq.SNDMORE)          #Command
                pub_sock.send(struct.pack("<ffff", 20, i / 4.0, 40, 40))


                pub_sock.send('draw', zmq.SNDMORE)     #Command Type
                pub_sock.send('fill')          #Command


            pub_sock.send('draw', zmq.SNDMORE)     #Command Type
            pub_sock.send('restore')          #Command


            pub_sock.send("draw", zmq.SNDMORE)
            pub_sock.send('select_font_face', zmq.SNDMORE)
            pub_sock.send(struct.pack("<sii", "Purisa", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD))


            pub_sock.send("draw", zmq.SNDMORE)
            pub_sock.send('set_font_size', zmq.SNDMORE)
            pub_sock.send(struct.pack("<f", 128))


            pub_sock.send("draw", zmq.SNDMORE)
            pub_sock.send('show_text', zmq.SNDMORE)
            pub_sock.send("Frame {}".format(frame))


            pub_sock.send('draw', zmq.SNDMORE)     #Command Type
            pub_sock.send('fill')          #Command



            pub_sock.send('draw', zmq.SNDMORE)   #Command Type
            pub_sock.send('finish')               #Command

            time.sleep(1.0 / 60.0)

    pub_sock.send('draw', zmq.SNDMORE)   #Command Type
    pub_sock.send('quit')               #Command


        

def main():
    print 'Sending...'
    
    context = zmq.Context()
    thread_pub = threading.Thread(target=pub_function, args=(context,))
    thread_pub.daemon=True
    thread_pub.start()
    
    while True:
        time.sleep(1)
    sys.exit(0)

        
        
if __name__ == "__main__":    
    main()
