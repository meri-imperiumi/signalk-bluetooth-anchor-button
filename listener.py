#!/usr/bin/python3 -u
import asyncio
import threading 
import os
import sys
from evdev import InputDevice, categorize, ecodes

dev = InputDevice('/dev/input/event1')
print("Connected to button")

clicks = 0
timer = None
def count_clicks():
    global clicks, timer
    if clicks > 1:
        print("Double click")
    else:
        print("Click")
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
