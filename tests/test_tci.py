import numpy as np
import pytest

from pywerami.api import GridData

from .conftest import make_tci_array


def test_parse_tci_degrees(tmp_path):
    tci = make_tci_array(ny=3, nx=3)
    gd = GridData._parse_tci(tci, degrees=True)

    assert gd.version == "7.0.8"
    assert gd.label == "foo.tci"
    assert gd.ind[0] == {"name": "T(C)", "min": 600.0, "max": 800.0, "num": 3}
    assert gd.ind[1] == {"name": "p(kbar)", "min": 1000.0, "max": 3000.0, "num": 3}
    assert gd.dep == ["Composition-SiO2", "Composition-Al2O3", "Density"]
    assert set(gd.data) == {"Composition-SiO2", "Composition-Al2O3", "Density"}

    base = np.arange(9, dtype=float)
    np.testing.assert_array_equal(gd.data["Density"], base)
    np.testing.assert_array_equal(gd.data["Composition-SiO2"], base)
    np.testing.assert_array_equal(gd.data["Composition-Al2O3"], base * 2)


def test_parse_tci_kelvin(tmp_path):
    tci = make_tci_array(ny=2, nx=2)
    gd = GridData._parse_tci(tci, degrees=False)

    assert gd.ind[0]["name"] == "T(K)"
    assert gd.ind[0]["min"] == pytest.approx(600.0 + 273.15)
    assert gd.ind[0]["max"] == pytest.approx(800.0 + 273.15)


def test_parse_tci_dep_data_reshapes_like_tab(tmp_path):
    tci = make_tci_array(ny=3, nx=3)
    gd = GridData._parse_tci(tci, degrees=True)

    var = gd.get_var("Density")
    assert var.shape == (3, 3)
    np.testing.assert_array_equal(var, np.arange(9, dtype=float).reshape(3, 3))


def test_from_tci_loads_file(monkeypatch, tmp_path):
    import scipy.io as sio

    tci = make_tci_array(ny=3, nx=3)
    calls = {}

    def fake_loadmat(filename, **kwargs):
        calls["filename"] = filename
        return {"pseudodata": tci.reshape(1, 1)}

    monkeypatch.setattr(sio, "loadmat", fake_loadmat)
    gd = GridData.from_tci(str(tmp_path / "data.tci"), degrees=True)

    assert calls["filename"] == str(tmp_path / "data.tci")
    assert gd.dep == ["Composition-SiO2", "Composition-Al2O3", "Density"]
