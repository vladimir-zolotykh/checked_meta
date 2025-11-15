#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
>>> class Movie(Checked):
...     title: str = ''
...     year: int = 0
...     box_office: float = 0.0
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
>>> Movie(title='Life of Brian')
Movie(title='Life of Brian', year=0, box_office=0.0)
>>> blockbuster = Movie(title='Avatar', year=2009, box_office=2000,
...                     director='James Cameron')
Traceback (most recent call last):
  ...
TypeError: got an unexpected keyword argument 'director'
>>> movie.director = 'Francis Ford Coppola'
Traceback (most recent call last):
  ...
AttributeError: 'Movie' object has no attribute 'director'
"""
from typing import get_type_hints, Callable, Any
from inspect import Signature, Parameter
import logging

logging.basicConfig(level=logging.WARNING)


class Descriptor:
    def __init__(self, name: str, constructor: Callable, default: Any = None):
        self._name = "_" + name
        self.constructor = constructor
        self.default = default

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
        if "__slots__" not in clsdict:
            __slots__ = []
            for name, constructor in annotations.items():
                default = clsdict.get(name, None)
                logging.info(
                    f"CheckedMeta.__new__ {clsname = }, {name = }, {default = }"
                )
                descriptor = Descriptor(name, constructor, default)
                clsdict[name] = descriptor
                __slots__.append(f"_{name}")
            logging.info(f"CheckedMeta.__new__ {__slots__ = }")
            clsdict["__slots__"] = __slots__

        return super().__new__(mcls, clsname, bases, clsdict)


def signature_from_dict(name_default: dict[str, Any]) -> Signature:
    parameters = [
        Parameter(name=name, kind=Parameter.POSITIONAL_OR_KEYWORD, default=default)
        for name, default in name_default.items()
    ]
    return Signature(parameters)


class Checked(metaclass=CheckedMeta):
    __slots__ = ()

    def __init__(self, **kwargs):
        sig = signature_from_dict(self.get_name_default())
        bound = sig.bind_partial(**kwargs)
        bound.apply_defaults()
        logging.info(f"Checked.__init__ {bound = }")
        for name, value in bound.arguments.items():
            setattr(self, name, value)

    @classmethod
    def get_name_default(cls) -> dict[str, Any]:
        res: dict[str, Any] = {}
        for name in get_type_hints(cls):
            value = cls.__dict__.get(name, None)
            if isinstance(value, Descriptor):
                value = value.default
            res[name] = value
        # res = {name: cls.__dict__.get(name, None) for name in get_type_hints(cls)}
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
