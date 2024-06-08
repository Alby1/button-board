# 2024/06/08 update
This is officially abandonware. Typing this just to let you know, tho I hope nobody (except for me) was actually using this software. This repo is proof of me failing as a programmer, but it's also a call to let everyone know, it's fine to have a project that went rogue. Never give up and never let yourself down.


# button-board
Windows program to use buttons of a controller to do actions on your computer.

Windows does not take exclusive control over gamepads, so keep in mind:
- this can run alongside games;
- games will still interpret input from the controller.
It's a double sided blade...

Proper documentation coming soon™.



# Requirements
## hidapi
Instructions in [Installation](#installation).

## Python 3.x
If you don't have Python already installed or don't know how to install it, the repository in its current state is not ready for you.

## Plugins
coming soon™


# Installation
- Clone this repo in an empty folder (folder A)
- Download hidapi-win from the latest release of hidapi from https://github.com/libusb/hidapi/releases/
- Copy `hidapi.dll` (either from x64 or x86, depending on your system) in this folder
- Write or download plugins in the same folder (folder A)
- (This part will be moved to the config file) Manually run board.py to list all the devices:
- - Search for the one you want to use
- - Modify parameters in `hid.Device(...)` in the connect_to_device function
- - Press the buttons you'd like to detect and see where they are.
- - Modify the subarray of read `list(d)[<start>:<end>]`, start should be the index of the first significant bit from step above divided by 8 and floored, end should be the index of the last significant bit from step above divided by 8 and floored.
- config (coming soon™)
- Run as module (`py -m button-board` from parent folder)
