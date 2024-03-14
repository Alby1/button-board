from .board import Board
from .configuration import Configuration
from .printer import Printer

import time
import multiprocessing
import curses
import os
import psutil
import subprocess
import pywinauto


def main(stdscr):
    combinations: dict = None
    plugins: dict = None
    board: Board = None
    combinations, plugins, board = load_requires()
    if combinations is None and plugins is None and board is None:
        return
    #multiprocessing.shared_memory.SharedMemory() # https://docs.python.org/3/library/multiprocessing.shared_memory.html
    
    curses.use_default_colors()
    curses.init_pair(1, -1, -1)
    
    printer = Printer(stdscr)

    printer.add_log("Welcome to button board by Malbyx!")

    last_combo = None
    disconnected_device = [False, False] # [is it disconnected?, was it logged?]
    while 1:
        read = board.read_data()
        printer.update()
        if(read):
            if(disconnected_device[0] and not disconnected_device[1]):
                printer.add_log("Device has disconnected")
                disconnected_device[1] = True
            if(read[0] == -1):
                disconnected_device[0] = True
                continue
            if(disconnected_device[0] and disconnected_device[1]):
                printer.add_log("Device reconnected")
                disconnected_device = [False, False]
            getch = stdscr.getch()
            if(getch == 114):
                combinations, plugins, board = load_requires()
                printer.add_log("Reloaded combinations and plugins")
            if(getch == 99):
                os.startfile(f"{os.getcwd()}\\config.json")
            
            #printer.print(read)
            last_active = None
            none_true = True
            for i in range(1, len(Board.buttons) + 1):
                if(read[Board.buttons[i]]):
                    if(last_active):
                        none_true = False
                        try:
                            combo = combinations[f"{last_active}-{i}"]
                            if(last_combo != combo):
                                combo_ = combo.split("/")
                                params = []
                                for p in range(2, len(combo_)):
                                    params.append(combo_[p])
                                #multiprocessing.Process(target=getattr(plugins[combo_[0]]["plugin"], combo_[1]), args=(params,)).start()
                                combo__ = getattr(plugins[combo_[0]]["plugin"], combo_[1])(params)
                                printer.add_log(f"{combo}{':' if combo__ else ''}{(combo__ if combo__ else '')}")
                                last_combo = combo
                        except Exception as e:
                            print(e)
                            last_combo = None
                            continue
                    else:
                        
                        comb_keys = combinations.keys()
                        possible_combo = [f"You're pressing: {i}"]
                        for ck in comb_keys:
                            ck: str
                            
                            if ck.startswith(f"{i}-"):
                                possible_combo.append(f"{ck}: {combinations[ck]}")
                            if ck.endswith(f"-{i}"):
                                possible_combo.append(f"{ck}: {combinations[ck]}")

                        possible_combo.append("")

                        printer.updated = False
                        printer.update()
                        # or
                        #printer.clear_print()

                        printer.print("\n".join(possible_combo))

                    last_active = i
            if(none_true):
                last_combo = None
            time.sleep(0.001)




def load_requires():
    combinations: dict = None
    plugins: dict = None
    board: Board = None

    configurations = Configuration()
    
    combinations, plugins = configurations.read_file("config.json")

    for k in plugins.keys():
        plugins[k]["plugin"] = (__import__(k)).Plugin(plugins[k])

        if("process_name" in plugins[k].keys() and "process_path" in plugins[k].keys() and plugins[k]["process_name"] is not None and plugins[k]["process_path"] is not None):
            if(plugins[k]["process_name"] not in (p.name() for p in psutil.process_iter())):
                p = subprocess.Popen(['cmd.exe', '/c', rf'{plugins[k]["process_path"]}'])
                time.sleep(5)
                

    # https://pythonhosted.org/watchdog/quickstart.html#quickstart

    board = Board()

    while True:
        try:
            board.connect_to_device() # add error message to this, like for the live disconnect detection
            break
        except KeyboardInterrupt:
            return None, None, None
        except:
            pass


    return combinations, plugins, board



curses.wrapper(main)