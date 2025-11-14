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
    def __init__(self, title, year, box_office):
        self.title = title
        self.year = year
        self.box_office = box_office

    title: str
    year: int
    box_office: float


if __name__ == "__main__":
    print(get_type_hints(Movie))
    movie = Movie(title="The Godfather", year=1972, box_office=137)
    # movie = Movie()
    print(movie.__annotations__)
