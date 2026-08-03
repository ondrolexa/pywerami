import numpy as np
import pytest

from pywerami.api import GridData

from .conftest import make_tab


def test_from_tab_basic(tmp_path):
    path = tmp_path / "data.tab"
    make_tab(path)
    gd = GridData.from_tab(str(path), degrees=False)

    assert gd.version == "Test version"
    assert gd.label == "Test label"
    assert gd.xvar == 0
    assert gd.yvar == 1
    assert gd.ind[0] == {"name": "T(K)", "min": 500.0, "max": 700.0, "num": 3}
    assert gd.ind[1] == {"name": "P(bar)", "min": 1000.0, "max": 1400.0, "num": 3}
    assert gd.dep == ["V", "G"]
    assert set(gd.data) == {"V", "G"}
    np.testing.assert_array_equal(gd.data["V"], np.arange(9))
    np.testing.assert_array_equal(gd.data["G"], np.arange(9))


def test_from_tab_degrees_conversion(tmp_path):
    path = tmp_path / "data.tab"
    make_tab(path)
    gd = GridData.from_tab(str(path), degrees=True)

    assert gd.ind[0]["name"] == "T(C)"
    assert gd.ind[0]["min"] == pytest.approx(500.0 - 273.15)
    assert gd.ind[0]["max"] == pytest.approx(700.0 - 273.15)


def test_from_tab_duplicate_dependent_names(tmp_path):
    path = tmp_path / "data.tab"
    make_tab(path, deps=("V", "V", "G"), rows=[[i, i, i] for i in range(9)])
    gd = GridData.from_tab(str(path), degrees=False)

    assert gd.dep == ["V1", "V2", "G"]
    assert set(gd.data) == {"V1", "V2", "G"}
    np.testing.assert_array_equal(gd.data["V1"], np.arange(9))
    np.testing.assert_array_equal(gd.data["V2"], np.arange(9))
    np.testing.assert_array_equal(gd.data["G"], np.arange(9))


def test_from_tab_axis_names_removed_from_dep(tmp_path):
    path = tmp_path / "data.tab"
    make_tab(path, deps=("T(K)", "P(bar)", "V"), rows=[[i, i, i] for i in range(9)])
    gd = GridData.from_tab(str(path), degrees=False)

    assert gd.dep == ["V"]


def test_from_tab_rejects_non_2d(tmp_path):
    path = tmp_path / "data.tab"
    make_tab(path, ni=3)
    with pytest.raises(Exception, match="Only 2d tables are supported now"):
        GridData.from_tab(str(path), degrees=False)


def test_get_xrange(tmp_path):
    path = tmp_path / "data.tab"
    make_tab(path)
    gd = GridData.from_tab(str(path), degrees=False)

    np.testing.assert_allclose(gd.get_xrange(), [500.0, 600.0, 700.0])
    np.testing.assert_allclose(
        gd.get_xrange(2), [500.0, 540.0, 580.0, 620.0, 660.0, 700.0]
    )
    np.testing.assert_allclose(gd.get_yrange(), [1000.0, 1200.0, 1400.0])
    assert gd.get_extent() == (500.0, 700.0, 1000.0, 1400.0)


def test_get_var_reshape(tmp_path):
    path = tmp_path / "data.tab"
    make_tab(path)
    gd = GridData.from_tab(str(path), degrees=False)

    var = gd.get_var("V")
    assert isinstance(var, np.ma.MaskedArray)
    assert var.shape == (3, 3)
    assert var.mask.sum() == 0
    np.testing.assert_array_equal(var, np.arange(9).reshape(3, 3))


def test_get_var_nan_mask(tmp_path):
    path = tmp_path / "data.tab"
    rows = [[i, np.nan if i % 2 else i] for i in range(9)]
    make_tab(path, rows=rows)
    gd = GridData.from_tab(str(path), degrees=False)

    var = gd.get_var("G")
    assert var.shape == (3, 3)
    np.testing.assert_array_equal(var.mask, np.arange(9).reshape(3, 3) % 2 == 1)
    np.testing.assert_array_equal(var.compressed(), [0, 2, 4, 6, 8])


def test_get_var_custom_nan_value(tmp_path):
    path = tmp_path / "data.tab"
    rows = [[i, -999 if i % 2 else i] for i in range(9)]
    make_tab(path, rows=rows)
    gd = GridData.from_tab(str(path), degrees=False)

    var = gd.get_var("G", nan=-999)
    assert var.shape == (3, 3)
    np.testing.assert_array_equal(var.mask, np.arange(9).reshape(3, 3) % 2 == 1)


def test_get_var_masks_nan_with_custom_marker(tmp_path):
    """NaN is always treated as missing, even when a different nan marker is set."""
    path = tmp_path / "data.tab"
    rows = [
        [i, -999 if i % 3 == 0 else (np.nan if i % 3 == 1 else i)] for i in range(9)
    ]
    make_tab(path, rows=rows)
    gd = GridData.from_tab(str(path), degrees=False)

    var = gd.get_var("G", nan=-999)
    expected = (np.arange(9) % 3 != 2).reshape(3, 3)
    np.testing.assert_array_equal(var.mask, expected)


def test_from_tab_roundtrip_via_get_var(tmp_path):
    """Row-major ordering: index = y * xnum + x."""
    path = tmp_path / "data.tab"
    rows = [[i, i * 10] for i in range(9)]
    make_tab(path, rows=rows)
    gd = GridData.from_tab(str(path), degrees=False)

    np.testing.assert_array_equal(gd.get_var("G"), (np.arange(9) * 10).reshape(3, 3))
