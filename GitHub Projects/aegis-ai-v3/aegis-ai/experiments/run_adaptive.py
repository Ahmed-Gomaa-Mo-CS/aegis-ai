"""Adaptive-attacker evaluation + adversarial hardening loop.

    python -m experiments.run_adaptive --seeds 10
Reports evasion rate (attacks that reach ALLOW) per defence configuration, then
re-attacks after the defender learns from the attacker's successful evasions.
"""
import argparse
import logging
import statistics as st

from config.settings import Config
from aegis.core.system import AegisSystem
from aegis.simulation.attacker import EventGenerator
from aegis.simulation.adaptive_attacker import AdaptiveAttacker


def probe_fn(system):
    def probe(payload):
        decision, _ = system.engine.evaluate({"payload": payload})   # no learning during probing
        return decision
    return probe


def attack_round(system, attacks, atk):
    probe = probe_fn(system)
    wins = []
    for e in attacks:
        ok, final, q = atk.evade(probe, e["payload"])
        if ok:
            wins.append(final)
    return wins


def run(cfg, seeds, warm=300, n_attacks=40, max_queries=12, harden=False):
    before, after, queries = [], [], []
    for s in range(seeds):
        system = AegisSystem(cfg, seed=s)
        system.run(EventGenerator(s).stream(warm))               # normal operation / warm-up
        pool = [e for e in EventGenerator(1000 + s).stream(400) if e["malicious"]][:n_attacks]
        atk = AdaptiveAttacker(seed=s, max_queries=max_queries)
        wins = attack_round(system, pool, atk)
        before.append(len(wins) / len(pool))
        if harden:                                               # learn from successful evasions
            for w in wins:
                system.llm.store.add(w, "block") if system.llm else None
                if "ML-Agent" in system.agents:
                    system.agents["ML-Agent"].fit_one(w, True)
            fresh = [e for e in EventGenerator(5000 + s).stream(400) if e["malicious"]][:n_attacks]
            wins2 = attack_round(system, fresh, AdaptiveAttacker(seed=s + 500, max_queries=max_queries))
            after.append(len(wins2) / len(fresh))
    return st.mean(before), (st.mean(after) if after else None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=10)
    a = ap.parse_args()
    logging.basicConfig(level=logging.ERROR)
    base = Config()
    rows = [("IDS only", base.with_(agents=("ids",), cascade=False)),
            ("ML only", base.with_(agents=("ml",), cascade=False)),
            ("LLM only (k=3)", base.with_(agents=("llm",), cascade=False)),
            ("Cascade, no LLM", base.with_(agents=("ids", "ml", "ai"))),
            ("Cascade + LLM", base),
            ("All agents, no cascade", base.with_(cascade=False))]
    print(f"{'defence':<26}{'evasion rate':>14}{'after hardening':>18}")
    for name, cfg in rows:
        b, h = run(cfg, a.seeds, harden=True)
        print(f"{name:<26}{b:>14.2f}{h:>18.2f}")


if __name__ == "__main__":
    main()
