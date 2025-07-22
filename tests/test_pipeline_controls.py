import pytest
from pytestqt.qtbot import QtBot
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from niaaml_gui.widgets.pipeline_controls import PipelineControlsWidget
from niaaml_gui.widgets.pipeline_canvas import PipelineCanvas


@pytest.fixture
def controls(qtbot: QtBot):
    widget = PipelineControlsWidget()
    qtbot.addWidget(widget)
    return widget


def test_run_button_initially_disabled(controls):
    assert controls.run_button.isEnabled() is False


def test_enable_disable_run_button(controls):
    controls.setRunEnabled(True)
    assert controls.run_button.isEnabled() is True

    controls.setRunEnabled(False)
    assert controls.run_button.isEnabled() is False


def test_run_button_emits_signal(controls, qtbot):
    with qtbot.waitSignal(controls.runClicked, timeout=1000):
        controls.setRunEnabled(True)
        qtbot.mouseClick(controls.run_button, Qt.MouseButton.LeftButton)



@pytest.fixture
def full_widget(qtbot: QtBot):
    canvas = PipelineCanvas()
    controls = PipelineControlsWidget()

    container = QWidget()
    layout = QVBoxLayout()
    layout.addWidget(canvas)
    layout.addWidget(controls)
    container.setLayout(layout)

    qtbot.addWidget(container)

    def update_run_button_state():
        ready = canvas.is_pipeline_ready()
        controls.run_button.setEnabled(ready)


    container.canvas = canvas
    container.controls = controls
    container.update_fn = update_run_button_state

    canvas.pipelineStateChanged.connect(update_run_button_state)

    return container


def test_update_run_button_state_false_when_incomplete(full_widget):
    canvas = full_widget.canvas
    controls = full_widget.controls
    update_fn = full_widget.update_fn

    canvas.add_config_block("Select CSV File") 
    update_fn()

    assert controls.run_button.isEnabled() is False


def test_update_run_button_state_true_when_ready(full_widget):
    canvas = full_widget.canvas
    controls = full_widget.controls
    update_fn = full_widget.update_fn

    canvas.add_config_block("Select CSV File")
    block = list(canvas.block_data.items())[0][1]
    block["path"] = "tests/tests_files/dataset_no_header_no_classes.csv"

    update_fn()

    assert controls.run_button.isEnabled() is True
