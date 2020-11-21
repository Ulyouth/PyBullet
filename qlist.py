# -*- coding: utf-8 -*-

"""
NAME:    qlist.py
AUTHOR:  Ulyouth
VERSION: 1.0.0
DATE:    15.10.2020 
DESC:    A class for thread synchronization using queues. 
"""

class QList:
    def __init__(self):
        self.q = []

    def put(self, data):
        self.q.append(data)

    def get(self):
        data = None

        try:
            data = self.q.pop(0)
        except IndexError:
            pass

        return data

    def empty(self):
        return len(self.q) == 0
