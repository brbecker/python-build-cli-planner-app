from abc import ABC, ABCMeta, abstractmethod
from collections.abc import Iterable
from datetime import datetime

from dateutil.parser import parse


class DeadlinedMetaReminder(Iterable, metaclass=ABCMeta):
    @abstractmethod
    def is_due(self):
        pass


class DeadlinedReminder(Iterable, ABC):
    @classmethod
    def __subclasshook__(cls, subclass):
        if cls is not DeadlinedReminder:
            return NotImplemented

        def attr_in_heirarchy(attr):
            return any(attr in SuperClass.__dict__ for SuperClass in subclass.__mro__)
        
        if not all(attr_in_heirarchy(attr) for attr in ('__iter__', 'is_due')):
            return NotImplemented

        return True

    @abstractmethod
    def is_due(self):
        pass


class DateReminder(DeadlinedReminder):
    def __init__(self, text: str, date: str) -> None:
        self.date = parse(date, dayfirst=True)
        self.text = text

    def __iter__(self):
        return iter([self.text, self.date.isoformat()])

    def is_due(self):
        return self.date <= datetime.now()
