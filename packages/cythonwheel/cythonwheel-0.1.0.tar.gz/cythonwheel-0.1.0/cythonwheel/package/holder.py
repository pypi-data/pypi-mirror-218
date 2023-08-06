from __future__ import annotations

import abc


class Holder(metaclass=abc.ABCMeta):

    def __init__(self, a):
        self.a = a
