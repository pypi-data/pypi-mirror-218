from threading import Thread
from collections.abc import Callable, Iterable, Mapping
from typing import Any

class ControlledThread(Thread):
    def __init__(self) -> None:
        super().__init__()
        self.__status = True
    
    def before_run(self): pass
    
    def after_run(self): pass
    
    def step(self):
        raise Exception("ControlledThread.step must implement.")
    
    def run(self):
        self.__status = True
        self.before_run()
        while self.__status:
            self.step()
        self.after_run()
        
    def stop(self):
        self.__status = False

if __name__ == '__main__':
    class __Test(ControlledThread):
        def step(self):
            print("hi")
            
    t = __Test()
    t.start()
    
    import time
    time.sleep(3)
    t.stop()