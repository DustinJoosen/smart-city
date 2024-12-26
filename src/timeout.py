import threading
import time


# Accepts a callback, and executes it after the delay.
class Timeout:
    def __init__(self, callback, delay, *args, **kwargs):
        self.callback = callback
        self.delay = delay
        self.args = args
        self.kwargs = kwargs
        
        threading.Thread(target=self._run).start()

    def _run(self):
        time.sleep(self.delay)
        self.callback(*self.args, **self.kwargs)

