#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import get_type_hints, Callable


class Descriptor:
    def __init__(self, name: str, constructor: Callable):
        self._name = "_" + name
        self.constructor = constructor

    def __get__(self, instance, owner=None):
        if not instance:
            return self
        return getattr(instance, self._name)

    def __set__(self, instance, value):
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


class Checked(metaclass=CheckedMeta):
    def __init__(self, **kwargs):
        for name in self.fields():
            setattr(self, name, kwargs.get(name, ...))

        # for name, value in kwargs.items():
        #     setattr(self, name, value)

    @classmethod
    def fields(cls):
        return get_type_hints(cls)

    def __repr__(self):
        pairs = [
            (k + "=" + repr(getattr(self, k)))
            for k, v in self.__class__.__annotations__.items()
        ]
        return f"{self.__class__.__name__}({', '.join(pairs)})"


class Movie(Checked):
    title: str
    year: int
    box_office: float


if __name__ == "__main__":
    movie = Movie(title="The Godfather", year=1972, box_office=137)
    # movie = Movie(title="The Godfather", year="long ago", box_office=137)
    print(movie)
