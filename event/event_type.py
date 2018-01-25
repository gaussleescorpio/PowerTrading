"""
This file contains the fundamental types of events
"""

from abc import ABC
from collections import defaultdict
from enum import Enum


class EventType(Enum):
    BarEvent = 0
    TickEvent = 1

    @classmethod
    def has_event(cls, name):
        return any(name == item.name for item in cls)


class Event(ABC):
    def __init__(self, type=None):
        self.type = type.name
        self.data = defaultdict()


class BarEvent(Event):
    def __init__(self, data):
        super().__init__(type=EventType.BarEvent)
        self.data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = defaultdict()
        try:
            self._data["High"] = data["High"]
            self._data["Open"] = data["Open"]
            self._data["Low"] = data["Low"]
            self._data["Close"] = data["Close"]
            self._data["Volume"] = data["Volume"]
            self._data["Date"] = data["Date"]
        except KeyError:
            raise ValueError("data input format error: not HOLCV")


class TickEvent(Event):
    def __init__(self, data, level=1):
        super().__init__(type=EventType.TickEvent)
        self.level = level
        self.data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = defaultdict()
        try:
            self._data["Time"] = data["Time"]
            for i in range(self.level):
                self._data["Ask%s" % str(i)] = data["Ask%s" % str(i)]
                self._data["Bid%s" % str(i)] = data["Bid%s" % str(i)]
        except KeyError:
            raise ValueError("check the assigned data if it is a tick data")





