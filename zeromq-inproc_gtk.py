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

import time
import threading
import struct
import sys

from gi.repository import Gtk, Gdk
import Queue
import cairo
import zmq


class MouseButtons:
    
    LEFT_BUTTON = 1
    RIGHT_BUTTON = 3
    
    
class CairoRecieverWindow(Gtk.Window):

    def __init__(self):
        super(CairoRecieverWindow, self).__init__()
        self.run = True
        self.recv_queue = Queue.Queue()
        self.draw_queue = Queue.Queue()
        self.init_ui()
        
        
    def init_ui(self):    

        self.darea = Gtk.DrawingArea()
        self.darea.connect("draw", self.on_draw)
        self.add(self.darea)
        
        self.set_title("Reciever window.")
        self.resize(300, 200)
        #self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", self.on_close)
        self.show_all()
        

    def on_close(self, wid, cr):
        
        self.run = False
    
    def on_draw(self, wid, cr):

        while True:
            try:
                cmd, args = self.draw_queue.get_nowait()
                if cmd == 'set_source_rgb':
                    cr.set_source_rgb(*args)
                elif cmd == 'set_source_rgba':
                    cr.set_source_rgba(*args)
                elif cmd == 'close_path':
                    cr.close_path()
                elif cmd == 'fill':
                    cr.fill()
                elif cmd == 'move_to':
                    cr.move_to(*args)
                elif cmd == 'select_font_face':
                    cr.select_font_face(*args)
                elif cmd == 'set_font_size':
                    cr.set_font_size(*args)
                elif cmd == 'show_text':
                    cr.show_text(args)
                elif cmd == 'rectangle':
                    cr.rectangle(*args)
                elif cmd == 'paint':
                    cr.paint()
                elif cmd == 'restore':
                    cr.restore()
                elif cmd == 'save':
                    cr.save()
                elif cmd == 'finish':
                    break
                else:
                    print 'Unknown cmd {}.{} '.format(cmd, args)
            except Queue.Empty:
                break
        

                         
                         
    def on_button_press(self, w, e):
        
        if e.type == Gdk.EventType.BUTTON_PRESS \
            and e.button == MouseButtons.LEFT_BUTTON:
            
            pass
            
        if e.type == Gdk.EventType.BUTTON_PRESS \
            and e.button == MouseButtons.RIGHT_BUTTON:
            
            self.darea.queue_draw()           
                                                        

    def sub_function(self, context):
        """ Definition of the SUB socket.

            It subscribes to a cmd_type and prints the messages of this cmd_type.
        """   
        #print "Subscribing to draw messages"
        sub_sock = context.socket(zmq.SUB)
        sub_sock.setsockopt(zmq.SUBSCRIBE, "draw") 
        sub_sock.connect("inproc://pushpub")

        while self.run:
            cmd_type    = sub_sock.recv()
            if sub_sock.rcvmore:
                cmd     = sub_sock.recv()
            args = None
            if sub_sock.rcvmore:
                if cmd in ["rectangle", "set_source_rgba"]:
                    args    = struct.unpack("<ffff", sub_sock.recv() )
                elif cmd in ["set_source_rgb", ]:
                    args    = struct.unpack("<fff", sub_sock.recv() )
                elif cmd in ["line_to", "move_to", ]:
                    args    = struct.unpack("<ff", sub_sock.recv() )
                elif cmd in ["set_font_size",]:
                    args    = struct.unpack("<f", sub_sock.recv() )
                elif cmd in ["fill", "close_path", "save", "restore",]:
                    args = None
                elif cmd in ["show_text",]:
                    args    = sub_sock.recv()
                elif cmd in ["select_font_face",]:
                    args    = struct.unpack("<sii", sub_sock.recv() )
                else:
                    args    = sub_sock.recv()
                
            #print "Recieved msg:{}  {}( {} )".format(cmd_type, cmd, args)
            
            if cmd == 'quit':
                print 'sub_function: quit'
                sub_sock.close()
                self.run = False
                break
            elif cmd == 'finish':
                #self.recv_queue.put( (cmd, args) )
                draw_queue = Queue.Queue()
                while True:
                    try:
                        (_cmd, _args) = self.recv_queue.get_nowait()
                        if _cmd == 'finish':
                            break
                        draw_queue.put((_cmd, _args))
                    except Queue.Empty:
                        break
                self.draw_queue = draw_queue
                self.darea.queue_draw()
            else:
                self.recv_queue.put( (cmd, args) )



    
def pub_function(context):
    """ Definition of the pub socket.

        It published messages in unidirectional way.
    """
    pub_sock = context.socket(zmq.PUB)
    pub_sock.bind("inproc://pushpub")

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

            pub_sock.send('draw', zmq.SNDMORE)     #Command Type
            pub_sock.send('save')          #Command


            pub_sock.send('draw', zmq.SNDMORE)   #Command Type
            pub_sock.send('set_source_rgba', zmq.SNDMORE)               #Command
            pub_sock.send(struct.pack("<ffff", 1, 1, 0, 1))


            pub_sock.send('draw', zmq.SNDMORE)     #Command Type
            pub_sock.send('paint')   #Command Type



            pub_sock.send('draw', zmq.SNDMORE)   #Command Type
            pub_sock.send('set_source_rgb', zmq.SNDMORE)               #Command
            pub_sock.send(struct.pack("<fff", 0, 0, 0))



            pub_sock.send("draw", zmq.SNDMORE)
            pub_sock.send('move_to', zmq.SNDMORE)
            pub_sock.send(struct.pack("<ff", 24, 24))



            pub_sock.send("draw", zmq.SNDMORE)
            pub_sock.send('select_font_face', zmq.SNDMORE)
            pub_sock.send(struct.pack("<sii", "Purisa", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD))


            pub_sock.send("draw", zmq.SNDMORE)
            pub_sock.send('set_font_size', zmq.SNDMORE)
            pub_sock.send(struct.pack("<f", 24))


            pub_sock.send("draw", zmq.SNDMORE)
            pub_sock.send('show_text', zmq.SNDMORE)
            pub_sock.send("Frame {}".format(frame))


            pub_sock.send('draw', zmq.SNDMORE)     #Command Type
            pub_sock.send('fill')          #Command


            pub_sock.send('draw', zmq.SNDMORE)   #Command Type
            pub_sock.send('set_source_rgb', zmq.SNDMORE)               #Command
            pub_sock.send(struct.pack("<fff", 1, 1, 1))

            pub_sock.send('draw', zmq.SNDMORE)     #Command Type
            pub_sock.send('rectangle', zmq.SNDMORE)          #Command
            pub_sock.send(struct.pack("<ffff", i / 4.0, i / 4.0, 40, 40))


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


            pub_sock.send('draw', zmq.SNDMORE)   #Command Type
            pub_sock.send('finish')               #Command

            time.sleep(1.0 / 60.0)

    pub_sock.send('draw', zmq.SNDMORE)   #Command Type
    pub_sock.send('quit')               #Command


        


def main():

    NUM_WINDOWS = 3
    
    context = zmq.Context()
    thread_pub = threading.Thread(target=pub_function, args=(context,))
    thread_pub.daemon=True
    thread_pub.start()

    windows = []
    for i in range(0, NUM_WINDOWS):
        windows.append( CairoRecieverWindow() )

    for window in windows:    
        thread_sub = threading.Thread(target=window.sub_function, args=(context,))
        thread_sub.daemon=True
        thread_sub.start()


    while windows:
        while Gtk.events_pending():
            Gtk.main_iteration()
        for window in windows:
            if not window.run:
                windows.remove(window)

        time.sleep(1.0 / 60.0)


    sys.exit(0)

        
        
if __name__ == "__main__":    
    main()
