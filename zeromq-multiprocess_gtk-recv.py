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

import argparse
import multiprocessing
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

    def __init__(self, device_offset=(0, 0), size=(300, 200)):
        super(CairoRecieverWindow, self).__init__()
        self.run = True
        self.recv_queue = Queue.Queue()
        self.draw_queue = Queue.Queue()
        self.init_ui()
        self._device_offset = device_offset
        self._size=size
        self.resize(*self._size)        
        
    def init_ui(self):    

        self.darea = Gtk.DrawingArea()
        self.darea.connect("draw", self.on_draw)
        self.add(self.darea)
        
        self.set_title("Reciever window.")

        #self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", self.on_close)
        self.show_all()
        


    def on_close(self, wid, cr):
        
        self.run = False
    
    def on_draw(self, wid, cr):
        t = cr.get_target()
        t.set_device_offset(*self._device_offset)
        while True:
            try:
                cmd, args = self.draw_queue.get_nowait()
                if cmd == 'set_source_rgb':
                    cr.set_source_rgb(*args)
                elif cmd == 'set_source_rgba':
                    cr.set_source_rgba(*args)
                elif cmd == 'rotate':
                    cr.rotate(*args)
                elif cmd == 'close_path':
                    cr.close_path()
                elif cmd == 'fill':
                    cr.fill()
                elif cmd == 'stroke':
                    cr.stroke()
                elif cmd == 'fill_preserve':
                    cr.fill_preserve()
                elif cmd == 'stroke_preserve':
                    cr.stroke_preserve()
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
                                                        

    def sub_function(self):
        """ Definition of the SUB socket.

            It subscribes to a cmd_type and prints the messages of this cmd_type.
        """   
        #print "Subscribing to draw messages"
        context = zmq.Context()
        sub_sock = context.socket(zmq.SUB)
        sub_sock.setsockopt(zmq.SUBSCRIBE, "draw") 
        sub_sock.connect("ipc:///tmp/cairo-pushpub")

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
                elif cmd in ["rotate", "set_font_size",]:
                    args    = struct.unpack("<f", sub_sock.recv() )
                elif cmd in ["stroke", "stroke_preserve", "fill", "fill_preserve", "close_path", "save", "restore",]:
                    args = None
                elif cmd in ["show_text", ]:
                    args    = sub_sock.recv()
                elif cmd in ["select_font_face",]:
                    args    = struct.unpack("<sii", sub_sock.recv() )
                else:
                    print 'Recieved unknown command {} {}'.format(cmd_type, cmd)
                    raise NotImplementedError()
                    #args    = sub_sock.recv()
                
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



    


        
def main():

    parser = argparse.ArgumentParser(description='Cairo Command Reciever.')
    parser.add_argument('--device-offset', help='', default="0.0, 0.0")
    parser.add_argument('--size', help='', default="0.0, 0.0")
    
    args = parser.parse_args()
    device_offset = [float(coord) for coord in args.device_offset.split(',') ]
    size = [float(coord) for coord in args.size.split(',') ]
    
    app = CairoRecieverWindow(device_offset=device_offset, size=size)

    thread_sub = threading.Thread(target=app.sub_function)
    thread_sub.daemon=True
    thread_sub.start()

    while app.run:
        while Gtk.events_pending():
            Gtk.main_iteration()

        time.sleep(1.0 / 60.0)
    sys.exit(0)

        
        
if __name__ == "__main__":    
    main()
