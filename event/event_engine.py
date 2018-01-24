"""
This file contains the event engine
"""
from threading import Thread
from queue import Queue
from collections import defaultdict


class StandardEventEngine(object):
    """
    The most standard event engine using a main streaming loop with an extra
    event handling thread
    """
    def __init__(self):
        # setup the event Queue
        self._event_queue = Queue()

        # setup the switch
        self._on = False

        # event handling thread
        self._event_thread = Thread(target=self._run)

        # strategy bucket
        self.strategy_bucket = defaultdict()

    def _run(self):
        pass

    def _process(self):
        pass

    def stop(self):
        """
        used to stop the whole event engine
        """
        self._on = False
        self._event_thread.join()

    def register_strategy(self, strategy, name):
        """
        A strategy is a class which at least includes OnBar or OnTick method.
        :param strategy: a strategy calss
        :return:
        """
        if hasattr(strategy, "OnBar"):
            pass
        elif hasattr(strategy, "OnTick"):
            pass
        else:
            raise ValueError("Invalid strategy")
        assert isinstance(name, str), "strategy name must be string"
        if name in self.strategy_bucket:
            raise KeyError("%s strategy already registered")
        self.strategy_bucket[name] = strategy

    def unregister_strategy(self, name):
        """
        remove the strategy with specified name
        :param name:
        :return:
        """
        assert isinstance(name, str), "target strategy name must be string"
        if name in self.strategy_bucket:
            self.strategy_bucket.pop(name)

    def insert_event(self, event):
        self._event_queue.put(event)






