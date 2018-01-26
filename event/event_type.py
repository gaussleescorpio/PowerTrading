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


class BarEvent(Event):
    def __init__(self, data, ticker):
        super().__init__(type=EventType.BarEvent)
        self.data = data
        self.ticker = ticker

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
            self._data["Adj_Close_Price"] = data["Adj_Close_Price"]
            self._data["Volume"] = data["Volume"]
            self._data["Time"] = data["Time"]
        except KeyError:
            raise ValueError("data input format error: not HOLCV")

    def __repr__(self):
        return str(self)

    def __str__(self):
        format_str = """Ticker name: %s High: %s, Open: %s,
                        Low: %s, Close: %s, adj_close: %s,
                        Volume: %s, Time: %s""" %(self._data["Ticker"],
                                                  self._data["High"],
                                                  self._data["Open"],
                                                  self._data["Low"],
                                                  self._data["Close"],
                                                  self._data["Adj_Close_Price"],
                                                  self._data["Volume"],
                                                  self._data["Time"])
        return format_str


class TickEvent(Event):
    def __init__(self, data, ticker, level=1):
        super().__init__(type=EventType.TickEvent)
        self.ticker = ticker
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
                self._data["Ask%s" % str(i + 1)] = data["Ask%s" % str(i + 1)]
                self._data["Bid%s" % str(i + 1)] = data["Bid%s" % str(i + 1)]
                self._data["Ask%s_Size" % str(i + 1)] = data["Ask%s_Size" % str(i + 1)]
                self._data["Bid%s_size" % str(i + 1)] = data["Bid%s_Size" % str(i + 1)]

        except KeyError:
            raise ValueError("check the assigned data if it is a tick data")

    def __repr__(self):
        return str(self)

    def __str__(self):
        for i in range(self.level):
            format_str = """Best_Ask: %s, BAsk_Size: %s,
                            Best_Bid: %s, BBid_Size: %s""" % (self._data["Ask1"],
                                                              self._data["Ask1_Size"],
                                                              self._data["Bid1"],
                                                              self._data["Bid1_Size"])
        return format_str







