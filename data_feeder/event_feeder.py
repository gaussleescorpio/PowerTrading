from abc import ABCMeta
from .base import AbstractBarPriceEventIterator, AbstractTickPriceEventIterator


class AbstractGenericPriceFeeder(object):
    """
    the generic price feeder is used to feed the event data into event engine and store the necessary data
    for future calculations.
    """
    __metaclass__ = ABCMeta

    def unsubscribe_ticker(self, ticker):
        """
        Unsubscribes the price handler from a current ticker symbol.
        """
        try:
            self.tickers.pop(ticker, None)
            self.tickers_data.pop(ticker, None)
        except KeyError:
            print(
                "Could not unsubscribe ticker %s "
                "as it was never subscribed." % ticker
            )

    def get_last_timestamp(self, ticker):
        """
        Returns the most recent actual timestamp for a given ticker
        """
        if ticker in self.tickers:
            timestamp = self.tickers[ticker]["Time"]
            return timestamp
        else:
            print(
                "Time for ticker %s is not "
                "available from the %s." % (ticker, self.__class__.__name__)
            )
            return None


class AbstractGenericTickPriceFeeder(AbstractGenericPriceFeeder):
    def _store_event(self, event):
        ticker = event.ticker
        self.tickers[ticker]["bid"] = event.data["Bid1"]
        self.tickers[ticker]["ask"] = event.data["Ask1"]
        self.tickers[ticker]["timestamp"] = event.data["Time"]

    def get_best_bid_ask(self, ticker):
        if ticker in self.tickers:
            bid = self.tickers[ticker]["bid"]
            ask = self.tickers[ticker]["ask"]
            return bid, ask
        else:
            print(
                "There is no such ticker %s subscribed" % ticker
            )
            return 0.0, 0.0


class AbstractGenericBarPriceFeeder(AbstractGenericPriceFeeder):
    def _store_event(self, event):
        ticker = event.ticker
        self.tickers[ticker]["close"] = event.data["Close"]
        self.tickers[ticker]["adj_close"] = event.data["Adj_Close_Price"]
        self.tickers[ticker]["timestamp"] = event.data["Time"]

    def get_last_close_price(self, ticker):
        if ticker in self.tickers:
            close = self.tickers[ticker]["close"]
            return close
        else:
            print(
                "There is no such ticker %s subscribed" % ticker
            )
            return None


class AbstractGenericFeeder(AbstractGenericPriceFeeder):
    def __init__(self, events_queue, price_event_iterator):
        self.events_queue = events_queue
        self.price_event_iterator = price_event_iterator
        self.continue_backtest = True
        self.tickers = {}
        for ticker in self.tickers_lst:
            self.tickers[ticker] = {}

    def stream_next(self):
        """
        Place the next PriceEvent (BarEvent or TickEvent) onto the event queue.
        """
        try:
            price_event = next(self.price_event_iterator)
        except StopIteration:
            self.continue_backtest = False
            return
        self._store_event(price_event)
        self.events_queue.put(price_event)

    @property
    def tickers_lst(self):
        return self.price_event_iterator.tickers_lst


class GenericBarFeeder(AbstractGenericFeeder, AbstractGenericBarPriceFeeder):
    pass


class GenericTickFeeder(AbstractGenericFeeder, AbstractGenericTickPriceFeeder):
    pass


def CreateGenericFeeder(events_queue, price_event_iterator):
    if isinstance(price_event_iterator, AbstractBarPriceEventIterator):
        return GenericBarFeeder(events_queue, price_event_iterator)
    elif isinstance(price_event_iterator, AbstractTickPriceEventIterator):
        return GenericTickFeeder(events_queue, price_event_iterator)
    else:
        raise NotImplementedError("price_event_iterator must be instance of")
