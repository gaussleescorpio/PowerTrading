
from .base import AbstractBarPriceEventIterator, AbstractTickPriceEventIterator


class PandasDataFrameBarEventIterator(AbstractBarPriceEventIterator):
    """
    PandasDataFrameBarEventIterator is designed to read a Pandas DataFrame like

                      Open        High         Low       Close    Volume   Adj Close
    Date
    2010-01-04  626.951088  629.511067  624.241073  626.751061   3927000  313.062468
    2010-01-05  627.181073  627.841071  621.541045  623.991055   6031900  311.683844
    2010-01-06  625.861078  625.861078  606.361042  608.261023   7987100  303.826685
    2010-01-07  609.401025  610.001045  592.651008  594.101005  12876600  296.753749
    ...                ...         ...         ...         ...       ...         ...
    2016-07-18  722.710022  736.130005  721.190002  733.780029   1283300  733.780029
    2016-07-19  729.890015  736.989990  729.000000  736.960022   1222600  736.960022
    2016-07-20  737.330017  742.130005  737.099976  741.190002   1278100  741.190002
    2016-07-21  740.359985  741.690002  735.830994  738.630005    969100  738.630005

    [1649 rows x 6 columns]

    with Open-High-Low-Close-Volume (OHLCV) data (bar)
    for one financial instrument and iterate BarEvents.
    """
    def __init__(self, df, ticker):
        """
        Takes the the events queue, ticker and Pandas DataFrame
        """
        self.data = df
        self.ticker = ticker
        self.tickers_lst = [ticker]
        self._itr_bar = self.data.iterrows()

    def __next__(self):
        index, row = next(self._itr_bar)
        price_event = self._create_event(self.ticker, row)
        return price_event


class PandasDataFrameTickEventIterator(AbstractTickPriceEventIterator):
    """
    PandasPanelBarEventIterator is designed to read a Pandas DataFrame like

                                   Bid        Ask
    Time
    2016-02-01 00:00:01.358  683.56000  683.58000
    2016-02-01 00:00:02.544  683.55998  683.58002
    2016-02-01 00:00:03.765  683.55999  683.58001
    ...
    2016-02-01 00:00:10.823  683.56001  683.57999
    2016-02-01 00:00:12.221  683.56000  683.58000
    2016-02-01 00:00:13.546  683.56000  683.58000

    with tick data (bid/ask)
    for one financial instrument and iterate TickEvents.
    """
    def __init__(self, df, ticker):
        """
        Takes the the events queue, ticker and Pandas DataFrame
        """
        self.data = df
        self.ticker = ticker
        self.tickers_lst = [ticker]
        self._itr_bar = self.data.iterrows()

    def __next__(self):
        index, row = next(self._itr_bar)
        level = len(row)/2
        price_event = self._create_event(self.ticker, row, level)
        return price_event