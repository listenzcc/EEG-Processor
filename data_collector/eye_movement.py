import time
import socket
import bisect

from threading import Thread, RLock
from .logging import logger

class EyeMovementData:
    data = []
    times = []
    n = 0
    lock = RLock()
    
    def reset_data(self):
        self.data = []
        self.times = []
        self.n = 0
        logger.info('Data is reset to empty.')
    
    def append_data(self, x, y, ld, rd):
        with self.lock:
            self.data.append([x, y, ld, rd])
            self.times.append(time.time())
            self.n += 1
            n = self.n
        if n % 1000 == 0:
            self.report_current_data_length()
    
    def report_current_data_length(self):
        logger.debug(f'Data length: {self.n}.')

    @logger.catch
    def fetch_data(self, length:float):
        '''
        Require data for length in seconds.
        
        :params length float: The length in seconds.
        
        :returns d: The required data.
        :returns t: The times of the required data.
        '''
        t2 = time.time()
        t1 = t2 - length
        with self.lock:
            try:
                assert self.n > 1, 'Not having enough data'
                # Find the latest times idx of > t1
                # The required length m is thus computed.
                # The bisect is applied since the times are sorted asscending already.
                m = self.n - bisect.bisect_right(self.times, t1)
                d = self.data[-m:]
                t = self.times[-m:]
                return d, t
            except:
                logger.warning('Eye movement data is empty.')
                return None, None
        

class TCPServer(EyeMovementData):
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host: str = 'localhost'
    port: int = 8080
    
    def __init__(self, **kwargs):
        super().__init__()
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
                logger.info(f'Set {k}={v}')
            logger.info(f'Initialize {self}')
            
    def _run_forever(self):
        '''
        Start receiving data.
        '''
        # Bind and listen to one clinet.
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        logger.info('Service establishes and is running forever')
        
        self.reset_data()
        while True:  
            client, addr = self.socket.accept()
            try:
                recv = client.recv(1024).decode()
                params = dict(p.split('=') for p in recv.strip().split('&'))
                x = float(params.get('x', 0))
                y = float(params.get('y', 0))
                ld = float(params.get('ld', 0))
                rd = float(params.get('rd', 0))
                self.append_data(x, y, ld, rd)
                
                pass
            except Exception as err:
                logger.exception(err)
            finally:
                client.close()
            pass 
        
    def start_service(self):
        logger.info('Start service')
        Thread(target=self._run_forever, daemon=True).start()