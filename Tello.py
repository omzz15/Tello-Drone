import threading 
import socket
import time
import cv2
import signal

class Tello:
    
    def __init__(self, 
                 vs_ip = '0.0.0.0', vs_port=11111, 
                 send_ip='192.168.10.1', send_port=8889, 
                 receive_ip='', receive_port=9000):
        self.current_frame = None
        self.response = None
        self.running = True
        self.cap = None
        self.send_address = (send_ip, send_port)
        self.receive_address = (receive_ip, receive_port)
        self.vs_address = 'udp://@' + vs_ip + ':' + str (vs_port)
        self.init_socket()
        
    def init_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.receive_address)
        self.recvThread = threading.Thread(target=self.command_callback)
        self.recvThread.start()
        self.send_command('command')

    def start_stream(self):
        self.send_command('streamon')
        self.streamThread = threading.Thread(target=self.cv2_stream_callback)
        self.streamThread.start()                
        
    def cv2_stream_callback(self):
        if self.cap == None:
            self.cap = cv2.VideoCapture(self.vs_address)
        if not self.cap.isOpened ():
            self.cap.open (self.vs_address)
        while True:
            ret, frame = self.cap.read ()
            self._process(frame)
            if cv2.waitKey (1)&0xFF == ord ('q'):
                self.running = False
                h = lambda x, y: print('signal handler')
                signal.signal(signal.SIGABRT, h)
                signal.alarm(3)
                break
        self.cap.release ()
        cv2.destroyAllWindows ()

    def _process(self, frame):
        frame = self.frame_pre_process(frame)
        self.frame_pre_process_show(frame)
        frame = self.frame_process(frame)
        self.frame_process_show(frame)
        frame = self.frame_post_process(frame)
        self.frame_post_process_show(frame)
                
    def frame_pre_process(self, frame):
        return frame

    def frame_process(self, frame):
        return frame

    def frame_post_process(self, frame):
        return frame

    def frame_pre_process_show(self, frame):
        pass
        
    def frame_process_show(self, frame):
        cv2.imshow ('frame', frame)
        
    def frame_post_process_show(self, frame):
        pass

    def takeoff(self):
        self.sock.sendto(b'takeoff', self.send_address)        

    def joystick(self, amt):
        cmd = ('rc ' + ' '.join(map(str, amt))).encode(encoding="utf-8")
        self.sock.sendto(cmd, self.send_address)       

    def down(self, amt):
        cmd = ('down ' + str(amt)).encode(encoding="utf-8")
        self.sock.sendto(cmd, self.send_address)       

    def up(self, amt):
        cmd = ('up ' + str(amt)).encode(encoding="utf-8")
        self.sock.sendto(cmd, self.send_address)       

    def right(self, amt):
        cmd = ('right ' + str(amt)).encode(encoding="utf-8")
        self.sock.sendto(cmd, self.send_address)       
        
    def left(self, amt):
        cmd = ('left ' + str(amt)).encode(encoding="utf-8")
        self.sock.sendto(cmd, self.send_address)        

    def forward(self, amt):
        cmd = ('forward ' + str(amt)).encode(encoding="utf-8")
        self.sock.sendto(cmd, self.send_address)        

    def backward(self, amt):
        cmd = ('back ' + str(amt)).encode(encoding="utf-8")
        self.sock.sendto(cmd, self.send_address)        
        
    def send_command(self, cmd, wait_sec=10):
        cmd = cmd.encode(encoding="utf-8")
        self.response = None
        self.sock.sendto(cmd, self.send_address)
        retry_cnt = wait_sec * 10
        while retry_cnt > 0:
            time.sleep(0.1)
            retry_cnt -= 1
            if self.response:
                break
        if retry_cnt == 0:
            raise Exception('No response from the Drone')
        return self.response

    def command_callback(self):
        while self.running: 
            try:
                data, server = self.sock.recvfrom(1518)
                self.response = data #data.decode(encoding="utf-8")
            except socket.error as e:
                print ('Error in command callback : %s' % e)
                #break

    def get_current_frame(self):
        return self.current_frame
        
    def close(self):
        self.send_command('streamoff')
        self.joystick([0, 0, 0, 0])
        self.send_command('land')
        time.sleep(0.5)
        self.sock.close()
