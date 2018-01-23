"""
This file contains the event engine
"""
from threading import Thread
from queue import Queue


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


    def _run(self):
        pass