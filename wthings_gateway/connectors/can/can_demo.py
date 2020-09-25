#!/usr/bin/python
# encoding:utf-8


"""
    @author Liberty
    @file   can_demo.py
    @time   2020/9/9 12:52
"""
from can import Notifier, BufferedReader, Message, CanError, ThreadSafeBus
import time


def can():
    interface = "socketcan"
    channel = "vcan0"
    kwargs = {"fd": True}
    bus = ThreadSafeBus(interface=interface, channel=channel, **kwargs)
    reader = BufferedReader()
    bus_notifier = Notifier(bus, [reader])
    while True:
        message = reader.get_message()
        print("message=", message)
        time.sleep(0.5)

if __name__ == '__main__':
    can()
