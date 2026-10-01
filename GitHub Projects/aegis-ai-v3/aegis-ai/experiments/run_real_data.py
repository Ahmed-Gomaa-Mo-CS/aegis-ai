"""Run the pipeline on a REAL labelled dataset (CSV or JSONL with columns text,label; label 1 = malicious).

    # e.g. export deepset/prompt-injections or Tensor Trust to data/train.jsonl, data/test.jsonl
    python -m experiments.run_real_data --train data/train.jsonl --test data/test.jsonl \
        --backend gemini --k 3 --max-test 200

Train split -> ML agent + few-shot seed pool (day-0 knowledge). Test split -> evaluation stream.
Gemini calls cost money: start with --max-test 50.
"""
import argparse
import csv
import json
import logging
import random

from config.settings import Config
from aegis.core.system import AegisSystem


def load(path):
    rows = []
    if path.endswith(".jsonl"):
        with open(path, encoding="utf-8") as f:
            raw = [json.loads(l) for l in f if l.strip()]
    else:
        with open(path, encoding="utf-8", newline="") as f:
            raw = list(csv.DictReader(f))
    for r in raw:
        rows.append({"payload": str(r["text"]), "malicious": int(r["label"]) == 1, "type": "real", "novel": None})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", required=True)
    ap.add_argument("--test", required=True)
    ap.add_argument("--backend", choices=["sim", "gemini"], default="gemini")
    ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--max-test", type=int, default=200)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    logging.basicConfig(level=logging.WARNING)
    try:                                     # optional: read GEMINI_API_KEY from .env
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    train, test = load(a.train), load(a.test)
    rnd = random.Random(a.seed)
    rnd.shuffle(train)
    rnd.shuffle(test)
    test = test[:a.max_test]
    cfg = Config(llm_backend=a.backend, k_shots=a.k)
    system = AegisSystem(cfg, seed=a.seed, day0_events=train)
    s = system.run(test)
    print({k: round(v, 3) for k, v in s.items()})
    system.coordinator.trust_model.report()


if __name__ == "__main__":
    main()
