import ctypes

from pathlib import Path
source_path = Path(__file__).resolve().parent

ctypes.CDLL(f"{source_path}\\hidapi.dll")

import hid
import time

def access_bit(data, num):
    base = int(num // 8)
    shift = int(num % 8)
    return (data[base] >> shift) & 0x1



class Board():
    buttons = {
        1: 4,
        2: 5,
        3: 6,
        4: 7,
        5: 8,
        6: 9,
        7: 10,
        8: 11,
        9: 12,
        10: 13
    }

    def list_devices(self):
        for device_dict in hid.enumerate():
            keys = list(device_dict.keys())
            keys.sort()
            for key in keys:
                print("%s : %s" % (key, device_dict[key]))
            print()


    def connect_to_device(self):
        try:
            h = hid.Device(pid=6,vid=121)

            self.device = h
            h.nonblocking = 1
            time.sleep(0.05)

        except IOError as ex:
            print(ex)

    def read_data(self, debug = False) -> list[1|0]:
        try:
            d = self.device.read(32)
            if d:
                if(not debug):
                    d = (list(d)[5:7])
                d = [access_bit(d,i) for i in range(len(d)*8)]
                return d
        except:
            try:
                self.connect_to_device()
            except:
                return [-1]

    def disconnect_device(self):
        print("Closing the device")
        self.device.close()


if __name__ == "__main__":
    board = Board()
    try:
        board.connect_to_device()
        while 1:
            try:
                print(board.read_data(True))
                time.sleep(0.005)
            except KeyboardInterrupt:
                break
    except:
        board.list_devices()