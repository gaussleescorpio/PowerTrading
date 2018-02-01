from abc import ABCMeta


class GenericPriceFeeder(object):
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

