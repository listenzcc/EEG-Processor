"""
File: main.py
Author: Chuncheng Zhang
Date: 2025-05-08
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Main enter.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-05-08 ------------------------
# Requirements and constants
import time

from data_collector.neuroscan import Client
from data_collector.eye_movement import TCPServer
from data_collector.joint import align_joint_eeg_em_data


# %% ---- 2025-05-08 ------------------------
# Function and class
class StopWatch:
    # The window length to acquire in seconds.
    window_length: float = 4
    # The tick interval in seconds.
    interval: float = 1
    # The total length of the experiment.
    total: float = 10

# Connection to Neuroscan EEG device.
eeg_kwargs = dict(
    host='192.168.31.79',
    port=4000
)

# Connection from the eyemovement device.
em_kwargs = dict(
    host='localhost',
    port=8080
)

# %% ---- 2025-05-08 ------------------------
# Play ground
if __name__ == '__main__':
    eeg = Client(**eeg_kwargs)
    eeg.start_receiving_thread()
    
    em = TCPServer(**em_kwargs)
    em.start_service()

    sw = StopWatch()
    # for i in range(int(sw.total / sw.interval+1)):
    def receiving():
        while True:
            time.sleep(sw.interval)
            eeg_d, eeg_t = eeg.fetch_data(sw.window_length)
            em_d, em_t = em.fetch_data(sw.window_length)
            data = align_joint_eeg_em_data(eeg_d, eeg_t, em_d, em_t)
            # TODO: Do something with the data.
            print(data.shape)            
            
    from threading import Thread
    Thread(target=receiving, daemon=True).start()

    # Wait for enter to be pressed.
    input('Press Enter to Escape.')
    eeg.stop_receiving_thread()

# %% ---- 2025-05-08 ------------------------
# Pending


# %% ---- 2025-05-08 ------------------------
# Pending
