from Queue import Queue
import zmq

def recieve(sub_sock):

    while True:
        print 'Start recieving...'
        cmd_type    = sub_sock.recv()
        print 'Got cmd_type {}'.format(cmd_type)
        if sub_sock.rcvmore:
            cmd     = sub_sock.recv()
        args = None

        print 'Recieve {} {}'.format(cmd_type, cmd)



def main():
    context = zmq.Context()
    sub_sock = context.socket(zmq.SUB)
    sub_sock.setsockopt(zmq.SUBSCRIBE, "Context") 
    sub_sock.setsockopt(zmq.SUBSCRIBE, "ImageSurface") 
    sub_sock.connect("ipc:///tmp/cairo-pushpub2")

    recieve(sub_sock)


if __name__ == '__main__':
    main()
