import time

__autor__ = "N0rmalUser"
__version__ = "0.1"

def _tagger(func):
    def wrapper(self, *args):
        i=0
        message = ''
        while i < len(args):
            if i == len(args)-1:
                qwe = f'{args[i]}'
            else:
                qwe = f'{args[i]}:'
            message = message + str(qwe) + ' '
            i+=1
        return func(self, f"{message}")
    return wrapper

def _printer(self, message: str) -> None:
    with open(self.file, "a") as f:
        f.write(f"{message}\n")
        print(message)

class NLogger():
    ct = time.time()
    def __init__(self, *logfile, ConsoleDate=False):
        """Методы класса Logger: debug -> d, error -> e, info -> i, settings -> s, warning -> w """
        self.file = logfile    
    

    @_tagger # debug
    def d(self, message) -> None:
        message = f'- DEBUG - {message}'
        _printer(self,message)
    
    @_tagger # error
    def e(self, message) -> None:
        message = f'- ERROR - {message}'
        _printer(self,message)
    
    @_tagger # info
    def i(self, message) -> None:
        message = f'- INFO - {message}'
        _printer(self,message)

    @_tagger # settings
    def s(self, message) -> None:
        message = f'- SETINGS - {message}'
        _printer(self,message)

    @_tagger # warning
    def w(self, message) -> None:
        message = f'- WARNING - {message}'
        _printer(self,message)

    @_tagger # warning
    def c(self, message) -> None:
        message = f'- CRITICAL - {message}'
        _printer(self,message)

    def getNames(self):
        return 'Методы класса Logger:\ndebug -> d\nerror -> e\ninfo -> i\nsettings -> s\nwarning -> w\ncritical -> c'
