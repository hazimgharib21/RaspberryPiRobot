import sys
import tty
import termios

class keyboardInput:

    def __init__(self):
        pass

    def readchar(self):
        self.fd = sys.stdin.fileno()
        self.old_setting = termios.tcgetattr(self.fd)
        try:
            tty.setraw(sys.stdin.fileno())
            self.ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, self.old_setting)
        if self.ch == '0x03':
            raise KeyboardInterrupt
        return self.ch

    def readkey(self, getchar_fn=None):
        self.fd = sys.stdin.fileno()
        self.old_setting = termios.tcgetattr(self.fd)
        try:
            tty.setraw(sys.stdin.fileno())
            self.ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_setting)
        if self.ch == '0x03':
            raise KeyboardInterrupt
        
        getchar = getchar_fn or self.ch
        self.c1 = getchar
        if ord(self.c1) != 0x1b:
            return self.c1
        self.c2 = getchar
        if ord(self.c2) != 0x5b:
            return self.c1
        self.c3 = getchar
        return chr(0x10 + ord(self.c3) - 65)

        
