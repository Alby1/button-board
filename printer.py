import curses

class Printer():
    def __init__(self, stdscr):
        stdscr.nodelay(1)
        
        self.righe = 0
        self.height = 0
        self.width = 0
        self.stdscr = stdscr
        self.log = []
        self.updated = True

        self.terminal_height()
        

    def clear(self):
        self.stdscr.clear()
        self.stdscr.refresh()
        self.righe = 0

    def update(self):
        if(not self.updated):
            righe = self.righe
            i = max(10, righe)
            sub_log = self.log[-self.height+i:]
            self.clear()
            for line in sub_log:
                self.stdscr.addstr(i, 0, line, curses.color_pair(1))
                i += 1
            self.stdscr.refresh()
            self.updated = True

    def add_log(self, message):
        self.log.append(str(message))
        self.updated = False

    def terminal_height(self):
        rows, cols = self.stdscr.getmaxyx()
        self.height = rows
        self.width = cols
    
    def print(self, message: str):
        self.terminal_height()
        try:
            message = str(message)
            a_capi = message.count('\n')
            righe = self.righe
            righe += 1 + a_capi
            if(righe <= self.height):
                self.stdscr.move(self.righe,0)
                self.stdscr.addstr(message, curses.color_pair(1))
                self.righe = righe
        except Exception as e:
            print(str(e))
            pass

        self.stdscr.refresh()

    def clear_print(self):
        self.terminal_height()
        for i in range(self.righe):
            for j in range(self.width):
                try:
                    self.stdscr.addstr("-", curses.color_pair(1))
                except: pass
        self.righe = 0
        self.stdscr.refresh()


class Action():
    def __init__(self, plugins: dict[str, object]):
        self.plugins = plugins