import pytest
from pytestqt.qtbot import QtBot

from niaaml_gui.widgets.pipeline_canvas import PipelineCanvas


@pytest.fixture
def canvas(qtbot: QtBot):
    widget = PipelineCanvas()
    qtbot.addWidget(widget)
    return widget


def test_add_config_block_emits_signal(canvas, qtbot):
    with qtbot.waitSignal(canvas.pipelineStateChanged, timeout=1000):
        canvas.add_config_block("Select CSV File")


def test_pipeline_ready_false_when_empty(canvas):
    canvas.block_data.clear()
    canvas.scene.clear()

    print("Block data keys:", canvas.block_data.keys())

    assert len(canvas.block_data) == 0
    assert not canvas.is_pipeline_ready()

