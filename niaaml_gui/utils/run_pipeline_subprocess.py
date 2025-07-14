import sys, pathlib, os
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from niaaml_gui.utils.pipeline_runner import run_pipeline

if __name__ == "__main__":
    import json

    args = json.loads(sys.stdin.read())

    def log_fn(msg):
        print(msg, flush=True)

    run_pipeline(
        csv_path=args["csv_path"],
        has_header=args["has_header"],
        contains_classes=args["contains_classes"],
        fitness_name=args["fitness_name"],
        pop_size=args["pop_size"],
        inner_pop=args["inner_pop"],
        evals=args["evals"],
        inner_evals=args["inner_evals"],
        opt_alg=args["opt_alg"],
        classifiers=args["classifiers"],
        fs_algorithms=args["fs_algorithms"],
        ft_algorithms=args["ft_algorithms"],
        log_fn=log_fn,
        save_path=pathlib.Path(args["save_path"]),
    )
