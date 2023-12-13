from solution import *


def test_reflect_x():
    assert Point(3, 0).reflect(2.5, 0) == Point(2, 0)
    assert Point(4, 0).reflect(2.5, 0) == Point(1, 0)
    assert Point(5, 0).reflect(2.5, 0) == Point(0, 0)
    assert Point(6, 0).reflect(2.5, 0) == Point(-1, 0)

    assert Point(2, 0).reflect(2.5, 0) == Point(3, 0)
    assert Point(1, 0).reflect(2.5, 0) == Point(4, 0)

    assert Point(0, 0).reflect(4.5, 0) == Point(9, 0)
    assert Point(9, 0).reflect(4.5, 0) == Point(0, 0)


def test_reflect_y():
    assert Point(0, 3).reflect(0, 2.5) == Point(0, 2)
    assert Point(0, 2).reflect(0, 2.5) == Point(0, 3)


def test_reflect_both():
    assert Point(1, 3).reflect(1.5, 2.5) == Point(2, 2)
    assert Point(2, 2).reflect(1.5, 2.5) == Point(1, 3)
