import curses

class Printer():
    def __init__(self, stdscr):
        self.righe = 0
        self.height = 0
        self.stdscr = stdscr
        self.log = []

    def clear(self):
        self.stdscr.clear()
        i = 10
        sub_log = self.log[-self.height+10:]
        for line in sub_log:
            self.stdscr.addstr(i, 0, line)
            i += 1
        self.stdscr.refresh()
        self.righe = 0

    def add_log(self, message):
        self.log.append(str(message))

    def terminal_height(self):
        rows, cols = self.stdscr.getmaxyx()
        self.height = rows
    
    def print(self, message: str):
        self.terminal_height()
        self.stdscr.move(0,0)
        try:
            message = str(message)
            a_capi = message.count('\n')
            righe = self.righe
            righe += 1 + a_capi
            if(righe <= self.height):
                self.stdscr.addstr(message)
                self.righe = righe
        except Exception as e:
            print(str(e))
            pass

        self.stdscr.refresh()
