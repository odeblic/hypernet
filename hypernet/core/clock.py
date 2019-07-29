"""Send tick events on given times"""
import event.event
import time


TICK_PERIOD = 1


class Clock(object):
    def __init__(self):
        self.__subscribers = set()
        self.__before = time.monotonic()

    #def subscribe(self, subscriber, interval=None, timepoint=None, duration=None):
    #    self.__subscribers[name] = interval
    def subscribe(self, subscriber):
        self.__subscribers.add(subscriber)

    #def unsubscribe(self, subscriber):
    #    del self.__subscribers[name]
    def unsubscribe(self, subscriber):
        if subscriber in self.__subscribers:
            self.__subscribers.add(subscriber)

    def on_schedule(self):
        now = time.monotonic()
        elapsed_time = now - self.__before
        if elapsed_time >= TICK_PERIOD:
            for subscriber in self.__subscribers:
                subscriber.on_event(event.event.make_tick())
            self.__before = now
