"""Test Point."""
from unittest import mock

import pytest

from pygeoif import geometry


def test_bounds():
    point = geometry.Point(1.0, 0.0)

    assert point.bounds == (1.0, 0, 1, 0)


def test_bounds3d():
    point = geometry.Point(1.0, 0.0, 3.0)  # pragma: no mutate

    assert point.bounds == (1, 0, 1, 0)


def test_xy():
    point = geometry.Point(1.0, 0.0)

    with pytest.raises(IndexError) as exc:
        point.z

    exc.match(r"This point has no z coordinate.")
    assert point.x == 1
    assert point.y == 0


def test_xyz():
    point = geometry.Point(1.0, 0.0, 2.0)

    assert point.x == 1
    assert point.y == 0
    assert point.z == 2


def test_repr2d():
    point = geometry.Point(1, 0)

    assert repr(point) == "Point(1, 0)"


def test_repr3d():
    point = geometry.Point(1.0, 2.0, 3.0)

    assert repr(point) == "Point(1.0, 2.0, 3.0)"


def test_wkt2d():
    point = geometry.Point(1, 0)

    assert str(point) == "POINT (1 0)"


def test_wkt3d():
    point = geometry.Point(1.0, 0.0, 3.0)

    assert str(point) == "POINT Z (1.0 0.0 3.0)"


def test_coords_get():
    point = geometry.Point(1.0, 0.0, 3.0)

    assert point.coords == ((1, 0, 3),)


def test_coords_set():
    point = geometry.Point(1.0, 0.0, 3.0)  # pragma: no mutate
    point.coords = ((4, 5),)

    assert point.coords == ((4, 5),)


def test_geo_interface():
    point = geometry.Point(0, 1, 2)

    assert point.__geo_interface__ == {
        "type": "Point",
        "bbox": (0, 1, 0, 1),  # pragma: no mutate
        "coordinates": (0.0, 1.0, 2.0),
    }


def test_from_dict():
    point = geometry.Point._from_dict({"type": "Point", "coordinates": (0.0, 1.0, 2.0)})

    assert point.coords == ((0, 1, 2),)


def test_from_dict_wrong_type():
    with pytest.raises(ValueError):
        geometry.Point._from_dict(
            {"type": "Xoint", "coordinates": (0.0, 1.0, 2.0)},  # pragma: no mutate
        )


def test_from_compatible():
    not_a_geometry = mock.Mock()
    not_a_geometry.__geo_interface__ = {
        "type": "Point",
        "bbox": (0, 1, 0, 1),  # pragma: no mutate
        "coordinates": (0.0, 1.0, 2.0),
    }

    point = geometry.Point._from_interface(not_a_geometry)

    assert point.coords == ((0, 1, 2),)