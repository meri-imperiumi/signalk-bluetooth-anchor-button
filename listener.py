#!/usr/bin/python3 -u
import asyncio
import threading 
import os
import sys
import requests
import time
import atexit
from evdev import InputDevice, categorize, ecodes, list_devices

# Change this to the ID of your button device
deviceId = 'b8:27:eb:a8:7c:1f'

# Give system time to set up the device
time.sleep(1)

devicePath = None
devices = [InputDevice(path) for path in list_devices()]
for device in devices:
    if device.phys == deviceId:
        devicePath = device.path
if devicePath == None:
    sys.exit("No device found")

dev = InputDevice(devicePath)

print("Connected to button")
os.system('echo %s | festival --tts' % 'Button online')

def shutdown():
  os.system('echo %s | festival --tts' % 'Button offline')
atexit.register(shutdown)

clicks = 0
timer = None
def count_clicks():
    global clicks, timer
    if clicks > 1:
        print("Double click, raise anchor")
        r = requests.post('http://localhost/plugins/anchoralarm/raiseAnchor', data = {})
        print(r.text)
    else:
        print("Click, drop anchor")
        r = requests.post('http://localhost/plugins/anchoralarm/dropAnchor', data = {})
        print(r.text)
    clicks = 0
    timer = None

async def helper(dev):
    global clicks, timer
    async for ev in dev.async_read_loop():
        if ev.type == ecodes.EV_KEY:
             data = categorize(ev)
             if data.keystate == 1 and data.scancode == 115:
                 clicks = clicks + 1
                 if not timer:
                     timer = threading.Timer(0.3, count_clicks)
                     timer.start()

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(helper(dev))
except OSError:
    print("Disconnected")
    sys.exit(0)
