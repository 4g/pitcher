import threading
import queue
import tempfile
import sys

import sounddevice as sd
import soundfile as sf
import numpy
assert numpy  


class Recorder(threading.Thread):
    def __init__(self, path=0):
        threading.Thread.__init__(self)
        self.path = path
        self.recording = False
        self.q = queue.Queue()
    
    def callback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        self.q.put(indata.copy())


    def run(self):
        self.recording = True
        device_info = sd.query_devices(None, 'input')
        samplerate = int(device_info['default_samplerate'])
        with sf.SoundFile(self.path, mode='x', samplerate=samplerate, channels=1) as file:
            with sd.InputStream(channels=1, callback=self.callback):
                while self.recording:
                    file.write(self.q.get())
     

    def stop(self):
        self.recording = False
