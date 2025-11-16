#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import pytest


from run import Checked


def test_field_descriptor_validation_type_error():
    class Cat(Checked):
        name: str
        weight: float

    with pytest.raises(TypeError) as e:
        felix = Cat(name="Felix", weight=None)  # noqa F481

    assert str(e.value) == "_weight cannot be set to None"


def test_field_descriptor_validation_value_error():
    class Cat(Checked):
        name: str
        weight: float

    with pytest.raises(TypeError) as e:
        felix = Cat(name="Felix", weight="half stone")  # noqa F481

    assert str(e.value) == "_weight cannot be set to 'half stone'"


def test_constructor_attribute_error():
    class Cat(Checked):
        name: str
        weight: float

    with pytest.raises(TypeError) as e:
        felix = Cat(name="Felix", weight=3.2, age=7)  # noqa F481

    assert str(e.value) == "got an unexpected keyword argument 'age'"


def test_assignment_attribute_error():
    class Cat(Checked):
        name: str
        weight: float

    felix = Cat(name="Felix", weight=3.2)
    with pytest.raises(AttributeError) as e:
        felix.color = "tan"

    assert str(e.value) == "'Cat' object has no attribute 'color'"
