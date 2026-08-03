import sys

import numpy as np
import pytest
from qtpy import QtCore, QtWidgets

from pywerami.mainapp import AboutDialog, OptionsForm, PyWeramiWindow, process_cl_args


@pytest.fixture
def ready_window(window):
    return window


def test_process_cl_args_no_arg(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["pywerami"])
    args, unparsed = process_cl_args()
    assert args.filename is None
    assert unparsed == []


def test_process_cl_args_with_file(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["pywerami", "data.tab", "--foo"])
    args, unparsed = process_cl_args()
    assert args.filename == "data.tab"
    assert unparsed == ["--foo"]


def test_window_ready_and_model(ready_window):
    w = ready_window
    assert w.ready
    assert w.data.dep == ["V", "G"]
    assert w._model.rowCount() == 2
    assert w._model.item(0).text() == "V"
    assert w._model.item(1).text() == "G"


def test_default_var_props(ready_window):
    w = ready_window
    w.default_var_props("V")
    prop = w.props["V"]
    assert prop["min"] == 0.0
    assert prop["max"] == 8.0
    assert prop["num"] == 10
    assert prop["levels"] == "num"
    assert prop["type"] == "linear"
    assert prop["fill"] is False
    assert prop["cbar"] is False
    assert prop["cmap"] == "viridis"
    assert prop["contours"] == "color"
    assert prop["label"] is False
    assert prop["resample"] == 1
    assert prop["median"] == 1
    assert prop["gauss"] == 0


def test_set_and_apply_props_roundtrip(ready_window):
    w = ready_window
    assert w.var == "V"
    w.set_var_props("V")
    assert w.levelmin.text() == "0.0"
    assert w.levelmax.text() == "8.0"
    assert w.levelnum.text() == "10"

    w.opacity.setValue(50)
    w.apply_props()
    assert w.props["V"]["opacity"] == 50

    w.set_var_props("V")
    assert w.opacity.value() == 50


def test_apply_props_contours_modes(ready_window):
    w = ready_window
    w.contcheckmap.setChecked(True)
    w.apply_props()
    assert w.props["V"]["contours"] == "map"

    w.contchecknone.setChecked(True)
    w.apply_props()
    assert w.props["V"]["contours"] == ""

    w.contcheckcolor.setChecked(True)
    w.apply_props()
    assert w.props["V"]["contours"] == "color"


def test_step_from_levels_enforces_minimum(ready_window):
    w = ready_window
    w.levelnum.setText("1")
    w.step_from_levels()
    assert w.levelnum.text() == "2"


def test_step_from_levels_clamps_min(ready_window):
    w = ready_window
    w.levelmax.setText("1.0")
    w.levelmin.setText("5.0")
    w.step_from_levels()
    assert w.levelmin.text() == "1.0"


def test_step_from_levels_updates_step_and_prop(ready_window):
    w = ready_window
    w.setlevels.setChecked(True)
    w.levelmin.setText("0.0")
    w.levelmax.setText("8.0")
    w.levelnum.setText("5")
    w.step_from_levels()
    assert float(w.levelstep.text()) == pytest.approx(2.0)
    assert w.props["V"]["step"] == pytest.approx(2.0)


def test_plot_2d_contour_color(ready_window):
    w = ready_window
    w._model.item(0).setCheckState(QtCore.Qt.CheckState.Checked)
    w.plot()
    assert len(w._ax.collections) > 0


def test_plot_2d_contour_map(ready_window):
    w = ready_window
    w.props["V"]["contours"] = "map"
    w._model.item(0).setCheckState(QtCore.Qt.CheckState.Checked)
    w.plot()
    assert len(w._ax.collections) > 0


def test_plot_2d_contour_none(ready_window):
    w = ready_window
    w.props["V"]["contours"] = ""
    w._model.item(0).setCheckState(QtCore.Qt.CheckState.Checked)
    w.plot()
    assert len(w._ax.collections) == 0
    assert len(w._ax.images) == 0


def test_plot_2d_fill(ready_window):
    w = ready_window
    w.props["V"]["fill"] = True
    w._model.item(0).setCheckState(QtCore.Qt.CheckState.Checked)
    w.plot()
    assert len(w._ax.images) == 1


def test_plot_2d_fill_with_colorbar(ready_window):
    w = ready_window
    w.props["V"]["fill"] = True
    w.props["V"]["cbar"] = True
    w._model.item(0).setCheckState(QtCore.Qt.CheckState.Checked)
    w.plot()
    assert len(w._fig.axes) > 1


def test_plot_2d_contour_labels(ready_window):
    w = ready_window
    w.props["V"]["label"] = True
    w._model.item(0).setCheckState(QtCore.Qt.CheckState.Checked)
    w.plot()
    assert len(w._ax.texts) > 0


def test_plot_2d_min_equal_max(ready_window):
    w = ready_window
    w.props["V"]["min"] = 5.0
    w.props["V"]["max"] = 5.0
    w._model.item(0).setCheckState(QtCore.Qt.CheckState.Checked)
    w.plot()
    assert len(w._ax.collections) > 0


def test_plot_2d_levels_step(ready_window):
    w = ready_window
    w.props["V"]["levels"] = "step"
    w.props["V"]["step"] = 2.0
    w._model.item(0).setCheckState(QtCore.Qt.CheckState.Checked)
    w.plot()
    assert len(w._ax.collections) > 0


def test_plot_2d_cdf_levels(ready_window):
    w = ready_window
    w.props["V"]["type"] = "cdf"
    w._model.item(0).setCheckState(QtCore.Qt.CheckState.Checked)
    w.plot()
    assert len(w._ax.collections) > 0


def test_plot_2d_filters(ready_window):
    w = ready_window
    w.props["V"]["resample"] = 2
    w.props["V"]["median"] = 2
    w.props["V"]["gauss"] = 1.0
    w._model.item(0).setCheckState(QtCore.Qt.CheckState.Checked)
    w.plot()
    assert len(w._ax.collections) > 0


def test_plot_3d(ready_window):
    w = ready_window
    w.action3D.setChecked(True)
    w.switch3d()
    assert len(w._ax.collections) > 0


def test_switch3d_back_and_forth(ready_window):
    w = ready_window
    w.action3D.setChecked(True)
    w.switch3d()
    w.action3D.setChecked(False)
    w.switch3d()
    assert w._ax.name == "rectilinear"


def test_restore_props(ready_window):
    w = ready_window
    w.opacity.setValue(50)
    w.apply_props()
    assert w.props["V"]["opacity"] == 50
    w.restore_props()
    assert w.props["V"]["opacity"] == 100
    assert w.opacity.value() == 100


def test_plotgrid(ready_window):
    w = ready_window
    w.plotgrid()
    assert any(line.get_visible() for line in w._ax.xaxis.get_gridlines())


def test_plotpan(ready_window):
    w = ready_window
    w.plotpan()
    assert w.actionZoom.isChecked() is False


def test_plotzoom(ready_window):
    w = ready_window
    w.plotzoom()
    assert w.actionPan.isChecked() is False


def test_save_and_open_project_roundtrip(ready_window, tmp_path):
    w = ready_window
    path = tmp_path / "proj.pwp"
    w.props["V"]["opacity"] = 50
    w.project = str(path)
    w.do_save()
    assert path.exists()

    w.props["V"]["opacity"] = 99
    w.openProject(False, projfile=str(path))
    assert w.props["V"]["opacity"] == 50
    assert w.project == str(path)


def test_save_project_as(ready_window, tmp_path, monkeypatch):
    w = ready_window
    path = tmp_path / "proj.pwp"
    monkeypatch.setattr(
        "pywerami.mainapp.QtWidgets.QFileDialog.getSaveFileName",
        lambda *a, **k: (str(path), ""),
    )
    w.saveProjectAs()
    assert w.project == str(path)
    assert path.exists()


def test_about_dialog(qapp):
    dlg = AboutDialog("0.3.0")
    assert "About" in dlg.windowTitle()
    dlg.close()


def test_options_form_roundtrip(qapp, isolated_qsettings, tmp_path, monkeypatch):
    monkeypatch.setattr(
        "pywerami.mainapp.QtWidgets.QMessageBox.warning", lambda *a, **k: None
    )
    form = OptionsForm()
    form.nan.setText("-999")
    form.degrees.setChecked(True)
    form.check()
    form.close()

    form2 = OptionsForm()
    assert form2.nan.text() == "-999"
    assert form2.degrees.isChecked()
    form2.close()


def test_options_form_rejects_invalid_nan(qapp, monkeypatch):
    monkeypatch.setattr(
        "pywerami.mainapp.QtWidgets.QMessageBox.warning", lambda *a, **k: None
    )
    form = OptionsForm()
    form.nan.setText("abc")
    form.check()
    assert form.result() == QtWidgets.QDialog.DialogCode.Rejected
    form.close()


def test_version_fallback(monkeypatch):
    import importlib

    import pywerami.mainapp as mainapp_mod

    def boom(name):
        raise mainapp_mod.imeta.PackageNotFoundError(name)

    monkeypatch.setattr(mainapp_mod.imeta, "version", boom)
    mod = importlib.reload(mainapp_mod)
    assert mod.__version__ == "not installed"


def test_close_event_save(ready_window, tmp_path, monkeypatch):
    from qtpy import QtGui

    w = ready_window
    path = tmp_path / "proj.pwp"
    w.project = str(path)
    w.changed = True
    monkeypatch.setattr(
        "pywerami.mainapp.QtWidgets.QMessageBox.question",
        lambda *a, **k: QtWidgets.QMessageBox.Save,
    )
    event = QtGui.QCloseEvent()
    w.closeEvent(event)
    assert path.exists()
    assert event.isAccepted()


def test_close_event_discard(ready_window, monkeypatch):
    from qtpy import QtGui

    w = ready_window
    w.changed = True
    monkeypatch.setattr(
        "pywerami.mainapp.QtWidgets.QMessageBox.question",
        lambda *a, **k: QtWidgets.QMessageBox.Discard,
    )
    event = QtGui.QCloseEvent()
    w.closeEvent(event)
    assert event.isAccepted()


def test_close_event_cancel(ready_window, monkeypatch):
    from qtpy import QtGui

    w = ready_window
    w.changed = True
    monkeypatch.setattr(
        "pywerami.mainapp.QtWidgets.QMessageBox.question",
        lambda *a, **k: QtWidgets.QMessageBox.Cancel,
    )
    event = QtGui.QCloseEvent()
    w.closeEvent(event)
    assert not event.isAccepted()


def test_import_data_via_dialog(ready_window, tab_file, monkeypatch):
    w = ready_window
    monkeypatch.setattr(
        "pywerami.mainapp.QtWidgets.QFileDialog.getOpenFileName",
        lambda *a, **k: (str(tab_file), ""),
    )
    w.import_data()
    assert w.data.label == "Test label"


def test_reimport_data(ready_window, tab_file):
    w = ready_window
    w.import_data(str(tab_file))
    assert w.data.label == "Test label"
    assert w._model.rowCount() == 2


def test_import_data_unsupported(ready_window):
    w = ready_window
    with pytest.raises(Exception, match="Unsupported file format"):
        w.import_data("file.xyz")


def test_save_project_first_time(ready_window, tmp_path, monkeypatch):
    w = ready_window
    path = tmp_path / "proj.pwp"
    monkeypatch.setattr(
        "pywerami.mainapp.QtWidgets.QFileDialog.getSaveFileName",
        lambda *a, **k: (str(path), ""),
    )
    w.saveProject()
    assert w.project == str(path)
    assert path.exists()


def test_save_project_as_appends_extension(ready_window, tmp_path, monkeypatch):
    w = ready_window
    target = str(tmp_path / "proj")
    monkeypatch.setattr(
        "pywerami.mainapp.QtWidgets.QFileDialog.getSaveFileName",
        lambda *a, **k: (target, ""),
    )
    w.saveProjectAs()
    assert w.project == target + ".pwp"


def test_open_project_via_dialog(ready_window, tmp_path, monkeypatch):
    w = ready_window
    path = tmp_path / "proj.pwp"
    w.props["V"]["opacity"] = 50
    w.project = str(path)
    w.do_save()
    w.changed = False
    w.props["V"]["opacity"] = 99
    monkeypatch.setattr(
        "pywerami.mainapp.QtWidgets.QFileDialog.getOpenFileName",
        lambda *a, **k: (str(path), ""),
    )
    w.openProject(False)
    assert w.props["V"]["opacity"] == 50


def test_open_project_prompts_save_when_changed(ready_window, tmp_path, monkeypatch):
    w = ready_window
    path = tmp_path / "proj.pwp"
    w.props["V"]["opacity"] = 50
    w.project = str(path)
    w.do_save()
    w.changed = True
    w.props["V"]["opacity"] = 99
    prompt = []
    monkeypatch.setattr(
        "pywerami.mainapp.QtWidgets.QMessageBox.question",
        lambda *a, **k: prompt.append(True) or QtWidgets.QMessageBox.Save,
    )
    monkeypatch.setattr(
        "pywerami.mainapp.QtWidgets.QFileDialog.getOpenFileName",
        lambda *a, **k: (str(path), ""),
    )
    w.openProject(False)
    assert prompt
    assert w.props["V"]["opacity"] == 99


def test_contours_color(ready_window, monkeypatch):
    from qtpy import QtGui

    w = ready_window
    monkeypatch.setattr(
        "pywerami.mainapp.QtWidgets.QColorDialog.getColor",
        lambda *a, **k: QtGui.QColor(255, 0, 0),
    )
    w.contours_color()
    assert "ff0000" in w.contcolor.styleSheet()


def test_set_var_props_branches(ready_window):
    w = ready_window
    prop = w.props["V"]
    prop["levels"] = "step"
    prop["type"] = "cdf"
    prop["fill"] = True
    prop["cbar"] = True
    prop["contours"] = "map"
    prop["label"] = True
    w.set_var_props("V")
    assert w.setstep.isChecked()
    assert w.cdflevel.isChecked()
    assert w.fillstyle.isChecked()
    assert w.checkCBar.isChecked()
    assert w.contcheckmap.isChecked()
    assert w.contlabel.isChecked()

    prop["contours"] = ""
    w.set_var_props("V")
    assert w.contchecknone.isChecked()


def test_on_var_changed_3d(ready_window):
    w = ready_window
    w.action3D.setChecked(True)
    selection = QtCore.QItemSelection(w._model.index(1, 0), w._model.index(1, 0))
    w.on_var_changed(selection)
    assert w.var == "G"
    assert len(w._ax.collections) > 0


def test_apply_props_all_fields(ready_window):
    w = ready_window
    w.set_var_props("V")
    w.fillstyle.setChecked(True)
    w.checkCBar.setChecked(True)
    w.contcheckmap.setChecked(True)
    w.contlabel.setChecked(True)
    w.resample.setValue(2)
    w.filtersize.setValue(3)
    w.filtersigma.setValue(1.5)
    w.clipmin.setText("1.0")
    w.clipmax.setText("7.0")
    w.apply_props()
    prop = w.props["V"]
    assert prop["fill"] is True
    assert prop["cbar"] is True
    assert prop["contours"] == "map"
    assert prop["label"] is True
    assert prop["resample"] == 2
    assert prop["median"] == 3
    assert prop["gauss"] == 1.5
    assert prop["clipmin"] == 1.0
    assert prop["clipmax"] == 7.0


def test_plot_3d_colorbar(ready_window):
    w = ready_window
    w.props["V"]["cbar"] = True
    w.action3D.setChecked(True)
    w.switch3d()
    assert len(w._fig.axes) > 1


def test_edit_options(ready_window, monkeypatch):
    w = ready_window
    called = []
    monkeypatch.setattr(
        "pywerami.mainapp.OptionsForm.exec",
        lambda self: called.append(True) or 0,
    )
    w.edit_options()
    assert called


def test_close_event_save_without_project(ready_window, monkeypatch):
    from qtpy import QtGui

    w = ready_window
    w.project = None
    w.changed = True
    monkeypatch.setattr(
        "pywerami.mainapp.QtWidgets.QMessageBox.question",
        lambda *a, **k: QtWidgets.QMessageBox.Save,
    )
    event = QtGui.QCloseEvent()
    w.closeEvent(event)
    assert not event.isAccepted()


def test_import_data_tci(ready_window, tmp_path, monkeypatch):
    from pywerami.api import GridData

    w = ready_window
    stub = GridData(
        "v",
        "tci label",
        [
            {"name": "T(K)", "min": 500.0, "max": 700.0, "num": 3},
            {"name": "P(bar)", "min": 1000.0, "max": 1400.0, "num": 3},
        ],
        0,
        1,
        ["V"],
        {"V": np.arange(9, dtype=float)},
    )

    def fake_from_tci(cls, filename, degrees=False):
        return stub

    monkeypatch.setattr(
        "pywerami.mainapp.GridData.from_tci", classmethod(fake_from_tci)
    )
    path = tmp_path / "data.tci"
    path.write_text("dummy")
    w.import_data(str(path))
    assert w.data.label == "tci label"


def test_save_project_appends_extension(ready_window, tmp_path, monkeypatch):
    w = ready_window
    target = str(tmp_path / "proj")
    monkeypatch.setattr(
        "pywerami.mainapp.QtWidgets.QFileDialog.getSaveFileName",
        lambda *a, **k: (target, ""),
    )
    w.saveProject()
    assert w.project == target + ".pwp"
    assert (tmp_path / "proj.pwp").exists()


def test_save_project_existing_project(ready_window, tmp_path, monkeypatch):
    w = ready_window
    path = tmp_path / "proj.pwp"
    w.project = str(path)
    monkeypatch.setattr(
        "pywerami.mainapp.QtWidgets.QFileDialog.getSaveFileName",
        lambda *a, **k: (_ for _ in ()).throw(AssertionError("dialog must not open")),
    )
    w.saveProject()
    assert path.exists()


def test_apply_props_levels_step_and_cdf(ready_window):
    w = ready_window
    w.set_var_props("V")
    w.setstep.setChecked(True)
    w.cdflevel.setChecked(True)
    w.apply_props()
    assert w.props["V"]["levels"] == "step"
    assert w.props["V"]["type"] == "cdf"


def test_main(monkeypatch):
    import pywerami.mainapp as mainapp_mod

    calls = {}

    class FakeApp:
        def __init__(self, argv):
            calls["argv"] = argv

        def exec(self):
            calls["exec"] = True
            return 0

    class FakeWindow:
        def __init__(self, filename):
            calls["filename"] = filename

        def show(self):
            calls["show"] = True

    monkeypatch.setattr(mainapp_mod.QtWidgets, "QApplication", FakeApp)
    monkeypatch.setattr(mainapp_mod, "PyWeramiWindow", FakeWindow)
    monkeypatch.setattr(
        mainapp_mod.sys, "exit", lambda code: calls.setdefault("exit", code)
    )
    monkeypatch.setattr(mainapp_mod.sys, "argv", ["pywerami", "data.tab"])
    mainapp_mod.main()
    assert calls["filename"] == "data.tab"
    assert calls["exec"] is True
    assert calls["show"] is True


def test_fill_survives_resample_with_mismatched_nan_setting(nan_window):
    w = nan_window
    w.settings.setValue("nan", "-999")
    w.props["G"]["fill"] = True
    w.props["G"]["resample"] = 2
    w._model.item(1).setCheckState(QtCore.Qt.CheckState.Checked)
    w.plot()
    assert len(w._ax.images) == 1
    assert w._ax.images[0].get_array().mask.mean() < 1.0


def test_process_var_does_not_spread_nan(window):
    w = window
    data = np.ma.array(
        [[1.0, np.nan, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]],
        mask=np.zeros((3, 3), dtype=bool),
    )
    w.props["G"]["resample"] = 2
    proc = w._process_var("G", data)
    assert not np.isnan(proc.data).any()
