<<<<<<< HEAD
"""Experiments: baselines, k-shot sweep, budget Pareto, fault tolerance.

    python -m experiments.run_experiments --seeds 20 --n 300 --backend sim
"""
import argparse
import csv
import json
import logging
import math
import os
import statistics as st

from config.settings import Config
from aegis.core.system import AegisSystem
from aegis.simulation.attacker import EventGenerator

KEYS = ["precision", "recall", "f1", "flag_f1", "cost", "llm_rate", "failures"]


def run_config(cfg, seeds, n, novel_frac=0.5):
    runs = []
    for s in range(seeds):
        events = EventGenerator(seed=s).stream(n, novel_frac)
        runs.append(AegisSystem(cfg, seed=s).run(events))
    out = {}
    for k in KEYS:
        xs = [r[k] for r in runs]
        out[k] = (st.mean(xs), 1.96 * st.stdev(xs) / math.sqrt(len(xs)) if len(xs) > 1 else 0.0)
    return out


def table(title, rows):
    print(f"\n=== {title} ===")
    print(f"{'config':<26}{'F1':>16}{'recall':>16}{'cost/event':>12}{'LLM%':>7}")
    for name, r in rows:
        print(f"{name:<26}{r['f1'][0]:>9.3f}±{r['f1'][1]:.3f}{r['recall'][0]:>9.3f}±{r['recall'][1]:.3f}"
              f"{r['cost'][0]:>12.1f}{100 * r['llm_rate'][0]:>7.1f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=20)
    ap.add_argument("--n", type=int, default=300)
    ap.add_argument("--backend", choices=["sim", "gemini"], default="sim")
    ap.add_argument("--novel-frac", type=float, default=0.5)
    a = ap.parse_args()
    logging.basicConfig(level=logging.ERROR)
    base = Config(llm_backend=a.backend)
    run = lambda cfg: run_config(cfg, a.seeds, a.n, a.novel_frac)
    results = {}

    # 1) baselines ------------------------------------------------------------
    rows = []
    for label, agents in [("IDS only", ("ids",)), ("ML only", ("ml",)), ("AI-heuristic only", ("ai",)),
                          ("LLM only (k=3)", ("llm",))]:
        rows.append((label, run(base.with_(agents=agents, cascade=False))))
    rows.append(("All agents, no cascade", run(base.with_(cascade=False))))
    rows.append(("Cascade, no LLM", run(base.with_(agents=("ids", "ml", "ai")))))
    rows.append(("Cascade + LLM (k=3)", run(base)))
    table("Baselines", rows)
    results["baselines"] = rows

    # 2) few-shot sweep ----------------------------------------------------------
    rows = []
    for k in (0, 2, 3, 5):
        rows.append((f"LLM only, k={k}", run(base.with_(agents=("llm",), cascade=False, k_shots=k))))
    rows.append(("LLM only, k=3, static mem", run(base.with_(agents=("llm",), cascade=False,
                                                              k_shots=3, memory_update=False))))
    table("Few-shot sweep (LLM agent alone)", rows)
    results["k_sweep"] = rows
    rows = [(f"Cascade+LLM, k={k}", run(base.with_(k_shots=k))) for k in (0, 2, 3, 5)]
    table("Few-shot sweep (inside cascade)", rows)
    results["k_sweep_cascade"] = rows

    # 2b) aggregation + stop-threshold ablation (where the real bottleneck showed up)
    rows = []
    for arb in (False, True):
        for sh, w in ((0.8, 0.8), (0.9, 1.0)):
            for nf in (0.5, 1.0):
                r = run_config(base.with_(llm_arbiter=arb, stop_share=sh, stop_weight=w), a.seeds, a.n, nf)
                rows.append((f"arb={int(arb)} stop={sh} novel={nf}", r))
    table("Aggregation ablation (vote vs LLM arbiter)", rows)
    results["arbiter"] = rows

    # 3) budget Pareto ---------------------------------------------------------------
    rows = [(f"budget={b}", run(base.with_(budget=b))) for b in (1, 6, 16, 46)]
    table("Budget sweep (cascade + LLM)", rows)
    results["budget"] = rows

    # 4) fault tolerance ------------------------------------------------------------------
    rows = [(f"LLM failure={p:.0%}", run(base.with_(llm_failure_rate=p))) for p in (0, 0.3, 0.6, 1.0)]
    table("Fault tolerance (sim backend)", rows)
    results["faults"] = rows

    # 5) label scarcity -----------------------------------------------------------------------
    rows = [(f"label_rate={p}", run(base.with_(label_rate=p))) for p in (1.0, 0.2, 0.0)]
    table("Delayed/scarce feedback", rows)
    results["labels"] = rows

    os.makedirs("results", exist_ok=True)
    with open("results/results.json", "w") as f:
        json.dump({sec: [(n, r) for n, r in rs] for sec, rs in results.items()}, f, indent=1)
    with open("results/results.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["section", "config"] + [f"{k}_{s}" for k in KEYS for s in ("mean", "ci95")])
        for sec, rs in results.items():
            for name, r in rs:
                w.writerow([sec, name] + [round(v, 4) for k in KEYS for v in r[k]])
    try:
        from experiments.plot_results import plot_all
        plot_all(results)
    except ImportError:
        print("matplotlib not installed: skipping plots")
=======

from aegis.core.system import AegisSystem
from experiments.plot_results import plot_comparison


def run_experiment(use_llm):

    system = AegisSystem(use_llm=use_llm)
    system.run_experiment(n=50)

    return system.metrics.compute(), system.metrics.history


def main():

    print("\n=== RUNNING WITHOUT LLM ===")
    no_llm_metrics, no_llm_history = run_experiment(False)

    print("\n=== RUNNING WITH LLM ===")
    llm_metrics, llm_history = run_experiment(True)

    print("\n=== COMPARISON ===")

    print("No LLM:", no_llm_metrics)
    print("With LLM:", llm_metrics)
>>>>>>> 1a004f91eda03eafd4e26b1cf9dbdc33beff3bbb


if __name__ == "__main__":
    main()
<<<<<<< HEAD
=======
plot_comparison(no_llm_metrics, llm_metrics)
>>>>>>> 1a004f91eda03eafd4e26b1cf9dbdc33beff3bbb
