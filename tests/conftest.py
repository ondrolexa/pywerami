import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import numpy as np
import pytest


def make_tab(
    path,
    xname="T(K)",
    xmin=500.0,
    xstep=100.0,
    xnum=3,
    yname="P(bar)",
    ymin=1000.0,
    ystep=200.0,
    ynum=3,
    deps=("V", "G"),
    rows=None,
    ni=2,
    version="Test version",
    label="Test label",
):
    lines = [version, label, str(ni)]
    for name, mn, step, num in (
        (xname, xmin, xstep, xnum),
        (yname, ymin, ystep, ynum),
    ):
        lines += [name, str(mn), str(step), str(num)]
    lines.append(str(len(deps)))
    lines.append(" ".join(deps))
    if rows is None:
        rows = [[i, i] for i in range(xnum * ynum)]
    for row in rows:
        lines.append(" ".join(str(v) for v in row))
    path.write_text("\n".join(lines) + "\n")


def make_tci_array(ny=3, nx=3, degrees=True):
    x = np.linspace(600, 800, nx)
    y = np.linspace(1000, 3000, ny)
    vals2d = np.arange(ny * nx, dtype=float).reshape(ny, nx)

    sd = np.empty((2, 1), dtype=object)
    sd[1, 0] = x.reshape(1, -1)
    sd[0, 0] = y.reshape(1, -1)

    paths = np.empty((1, 1), dtype=[("InputFilepath", "O")])
    paths["InputFilepath"][0, 0] = np.array(["/abs/dir/foo.tci"], dtype=object)

    comp = np.empty((1, 1), dtype=[("SiO2", "O"), ("Al2O3", "O")])
    comp["SiO2"][0, 0] = vals2d
    comp["Al2O3"][0, 0] = vals2d * 2

    tci = np.empty(
        1,
        dtype=[
            ("TCversion", "O"),
            ("paths", "O"),
            ("SectionDetails", "O"),
            ("Density", "O"),
            ("Composition", "O"),
        ],
    )
    tci["TCversion"][0] = np.array([["7.0.8"]], dtype=object)
    tci["paths"][0] = paths
    tci["SectionDetails"][0] = sd
    tci["Density"][0] = vals2d
    tci["Composition"][0] = comp
    return tci


@pytest.fixture(scope="session")
def qapp():
    from qtpy import QtWidgets

    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])
    return app


@pytest.fixture(autouse=True)
def isolated_qsettings(tmp_path):
    from qtpy import QtCore

    QtCore.QSettings.setDefaultFormat(QtCore.QSettings.IniFormat)
    QtCore.QSettings.setPath(
        QtCore.QSettings.IniFormat, QtCore.QSettings.UserScope, str(tmp_path)
    )


@pytest.fixture
def tab_file(tmp_path):
    path = tmp_path / "data.tab"
    make_tab(path)
    return path


@pytest.fixture
def griddata(tab_file):
    from pywerami.api import GridData

    return GridData.from_tab(str(tab_file), degrees=False)


@pytest.fixture
def window(qapp, tab_file, monkeypatch):
    from qtpy import QtWidgets
    from pywerami.mainapp import PyWeramiWindow

    monkeypatch.setattr(
        "pywerami.mainapp.QtWidgets.QFileDialog.getOpenFileName",
        lambda *a, **k: ("", ""),
    )
    monkeypatch.setattr(
        "pywerami.mainapp.QtWidgets.QMessageBox.question",
        lambda *a, **k: QtWidgets.QMessageBox.Discard,
    )
    w = PyWeramiWindow(str(tab_file))
    yield w
    w.close()


@pytest.fixture
def nan_window(qapp, tmp_path, monkeypatch):
    from qtpy import QtWidgets
    from pywerami.mainapp import PyWeramiWindow

    path = tmp_path / "data_nan.tab"
    rows = [[i, np.nan if i % 3 else i] for i in range(9)]
    make_tab(path, rows=rows)
    monkeypatch.setattr(
        "pywerami.mainapp.QtWidgets.QFileDialog.getOpenFileName",
        lambda *a, **k: ("", ""),
    )
    monkeypatch.setattr(
        "pywerami.mainapp.QtWidgets.QMessageBox.question",
        lambda *a, **k: QtWidgets.QMessageBox.Discard,
    )
    w = PyWeramiWindow(str(path))
    yield w
    w.close()
