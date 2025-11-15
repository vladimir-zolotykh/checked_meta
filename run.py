#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
>>> class Movie(Checked):
...     title: str
...     year: int
...     box_office: float
...
>>> movie = Movie(title='The Godfather', year=1972, box_office=137)
>>> movie.title
'The Godfather'
>>> movie
Movie(title='The Godfather', year=1972, box_office=137.0)
>>> blockbuster = Movie(title='Avatar', year=2009, box_office='billions')
Traceback (most recent call last):
  ...
TypeError: _box_office cannot be set to 'billions'
>>> movie.year = 'MCMLXXII'
Traceback (most recent call last):
  ...
TypeError: _year cannot be set to 'MCMLXXII'
"""
from typing import get_type_hints, Callable, Any
from inspect import Signature, Parameter


class Descriptor:
    def __init__(self, name: str, constructor: Callable):
        self._name = "_" + name
        self.constructor = constructor

    def __get__(self, instance, owner=None):
        if not instance:
            return self
        return getattr(instance, self._name)

    def __set__(self, instance, value):
        if value is (...):  # no value provided
            pass
        try:
            setattr(instance, self._name, self.constructor(value))
        except (TypeError, ValueError) as e:
            raise TypeError(f"{self._name} cannot be set to {value!r}") from e


class CheckedMeta(type):
    def __new__(mcls, clsname, bases, clsdict):
        annotations = clsdict.get("__annotations__", {})
        for name, constructor in annotations.items():
            clsdict[name] = Descriptor(name, constructor)

        return super().__new__(mcls, clsname, bases, clsdict)


def signature_from_dict(name_default: dict[str, Any]) -> Signature:
    parameters = [
        Parameter(name=name, kind=Parameter.POSITIONAL_OR_KEYWORD, default=default)
        for name, default in name_default.items()
    ]
    return Signature(parameters)


class Checked(metaclass=CheckedMeta):
    def __init__(self, **kwargs):
        sig = signature_from_dict(self.get_name_default())
        for name, value in sig.bind(**kwargs).arguments.items():
            setattr(self, name, value)

    @classmethod
    def get_name_default(cls) -> dict[str, Any]:
        res = {name: cls.__dict__.get(name, None) for name in get_type_hints(cls)}
        return res

    def __repr__(self):
        pairs = [
            (k + "=" + repr(getattr(self, k)))
            for k, v in self.__class__.__annotations__.items()
        ]
        return f"{self.__class__.__name__}({', '.join(pairs)})"


class Movie(Checked):
    title: str = ""
    year: int = 0
    box_office: float = 0.0


if __name__ == "__main__":
    import doctest

    doctest.testmod()
