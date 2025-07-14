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

        log(f"▶ Začenjam optimizacijo … [metric={fitness_name}, outer={evals}, inner={inner_evals}]")

        pipeline = pipeline_optimizer.run(
            fitness_name,
            pop_size, inner_pop,
            evals, inner_evals,
            opt_alg, opt_alg,
        )

        if pipeline is None:
            print(" pipeline_optimizer.run() returned None.")
        else:

            if save_path is not None:
                target_ppln = Path(save_path).with_suffix(".ppln")
                pipeline.export(target_ppln)
                target_txt = target_ppln.with_suffix("")
                pipeline.export_text(str(target_txt))
                
        return pipeline

    except Exception:
        traceback.print_exc()
        return None
