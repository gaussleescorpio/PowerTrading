"""
The basic iterator which is a fundamental type to mimic the real streaming data
"""
from ..event import event_type as ev


class AbstractPriceEventIterator(object):
    def __iter__(self):
        return self

    def next(self):
        return self.__next__()


class AbstractBarPriceEventIterator(AbstractPriceEventIterator):
    def _create_event(self, ticker, row):
        try:
            BarEvent = ev.BarEvent(row, ticker)
            return BarEvent
        except Exception:
            raise ValueError("Cannot form BarEvent...")


class AbstractTickPriceEventIterator(AbstractPriceEventIterator):
    def _create_event(self, ticker, row, level):
        try:
            Tickevent = ev.TickEvent(row, ticker, level)
            return Tickevent
        except Exception:
            raise ValueError("Cannot form TickEvent...")









