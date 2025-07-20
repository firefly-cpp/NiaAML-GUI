import traceback
from pathlib import Path
from typing import Callable, Sequence
from niaaml import PipelineOptimizer
from niaaml.data import CSVDataReader

def run_pipeline(
    *,
    csv_path: str,
    has_header: bool = True,
    contains_classes: bool = True,
    ignore_cols: list[int] | None = None,
    fitness_name: str,
    pop_size: int,
    inner_pop: int,
    evals: int,
    inner_evals: int,
    opt_alg: str,
    classifiers: Sequence[str],
    fs_algorithms: Sequence[str],
    ft_algorithms: Sequence[str],
    log_fn: Callable[[str], None] | None = None,
    save_path: Path | str | None = None,
):
    log = log_fn or (lambda *_: None)

    try:
        data_reader = CSVDataReader(
            src=csv_path,
            contains_classes=contains_classes,
            has_header=has_header,
        )

        pipeline_optimizer = PipelineOptimizer(
            data=data_reader,
            classifiers=list(classifiers) or ["RandomForest"],
            feature_selection_algorithms=list(fs_algorithms) or ["VarianceThreshold"],
            feature_transform_algorithms=list(ft_algorithms) or ["StandardScaler"],
            log=True
        )

        pipeline = pipeline_optimizer.run(
            fitness_name,
            pop_size, inner_pop,
            evals, inner_evals,
            opt_alg, opt_alg,
        )

        if pipeline is None:
            log(" pipeline_optimizer.run() returned None.")
            return None

        if save_path:
            save_dir = Path(save_path).resolve()
            save_dir.mkdir(parents=True, exist_ok=True)  

            target_ppln = save_dir / "NiaAML-GUI.ppln"
            target_txt  = save_dir / "NiaAML-GUI.txt"

            pipeline.export(target_ppln)
            pipeline.export_text(str(target_txt))

        return pipeline

    except Exception:
        traceback.print_exc()
        return None
