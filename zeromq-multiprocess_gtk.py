import subprocess
import threading

def run_reciever():
    cmd = ["python", "zeromq-multiprocess_gtk-recv.py"]
    subprocess.call(cmd)

def run_sender():
    cmd = ["python", "zeromq-multiprocess_gtk-send.py"]
    subprocess.call(cmd)



def main():
    NUM_RECIEVERS = 4

    for i in range(0, NUM_RECIEVERS):
        recieve_thread = threading.Thread(target=run_reciever)
        recieve_thread.daemon = True
        recieve_thread.start()

    run_sender()


if __name__ == '__main__':
    main()
