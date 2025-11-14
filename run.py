#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import get_type_hints


class CheckedMeta(type):
    def __new__(mcls, clsname, bases, clsdict):
        return super().__new__(mcls, clsname, bases, clsdict)


class Checked(metaclass=CheckedMeta):
    pass


class Movie(Checked):
    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)

    def __repr__(self):
        pairs = [
            (k + "=" + repr(getattr(self, k)))
            for k, v in self.__class__.__annotations__.items()
        ]
        return f"Movie({', '.join(pairs)})"

    title: str
    year: int
    box_office: float


if __name__ == "__main__":
    movie = Movie(title="The Godfather", year=1972, box_office=137)
    print(movie)
