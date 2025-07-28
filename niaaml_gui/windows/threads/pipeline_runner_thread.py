import subprocess
import json
from PyQt6.QtCore import QThread, pyqtSignal
import logging

class PipelineRunnerThread(QThread):
    ran = pyqtSignal(object)
    progress = pyqtSignal(str)

    def __init__(self, data):
        super().__init__()
        self._data = data
        nia_logger = logging.getLogger('NiaAML')
        nia_logger.setLevel(logging.INFO)
        
        class _QtHandler(logging.Handler):
            def emit(inner_self, record):
                self.progress.emit(record.getMessage())

        if not any(isinstance(h, _QtHandler) for h in nia_logger.handlers):
            nia_logger.addHandler(_QtHandler())

    def run(self):
        try:
            args = {
                "csv_path": self._data.csvSrc,
                "has_header": self._data.csvHasHeader,
                "contains_classes": True,
                "fitness_name": self._data.fitnessFunctionName,
                "pop_size": int(self._data.popSize or 0),
                "inner_pop": int(self._data.popSizeInner or 0),
                "evals": int(self._data.numEvals or 0),
                "inner_evals": int(self._data.numEvalsInner or 0),
                "opt_alg": self._data.optAlgName,
                "classifiers": self._to_list(self._data.classifiers),
                "fs_algorithms": self._to_list(self._data.fsas),
                "ft_algorithms": self._to_list(self._data.ftas),
                "save_path": self._data.outputFolder
            }

            process = subprocess.Popen(
                ["python", "-m", "niaaml_gui.utils.run_pipeline_subprocess"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            json.dump(args, process.stdin)
            process.stdin.close()

            for line in process.stdout:
                line = line.strip()
                self.progress.emit(line)

            process.wait()

            if process.returncode == 0:
                self.ran.emit("Pipeline finished successfully.")
            else:
                self.ran.emit("ERROR: Subprocess failed.")

        except Exception as e:
            import traceback
            traceback.print_exc()
            self.ran.emit(f"ERROR: {str(e)}")

    def _to_list(self, val):
        if isinstance(val, list):
            return val
        return [v.strip() for v in val.splitlines() if v.strip()]
