# Aegis-AI — Resource-Aware, Fault-Tolerant Multi-Agent Cyber Defense (research prototype)

Cheapest-first **cascade** of specialised agents (IDS → ML → AI-heuristic → few-shot LLM) under a
per-event **budget**, with Beta-Bernoulli **trust** weighting and an LLM agent that learns from
**2–5 retrieved examples** plus an online example memory.

## Run
    pip install -r requirements.txt
    python main.py --n 300 --k 3                 # one run (offline simulated-LLM backend)
    python -m experiments.run_experiments --seeds 20 --n 300
    python -m unittest discover -s tests -t .    # 17 tests
Real LLM: copy `.env.example` → `.env`, set `GEMINI_API_KEY`, add `--backend gemini`
(the Gemini backend is written against the SDK docs but **untested**; run it first).

## What each piece does
| Piece | File |
|---|---|
| Cumulative budget, cost per agent | `aegis/core/resource_controller.py` |
| Cascade, early stop, failure handling | `aegis/core/escalation_engine.py` |
| Few-shot retrieval (balanced labels) | `aegis/agents/example_store.py` |
| Prompt (delimited untrusted input), strict JSON parse, hard-case memory | `aegis/agents/llm_agent.py` |
| Backends: Gemini / offline proxy with fault injection | `aegis/agents/llm_backends.py` |
| Trust (Beta-Bernoulli + forgetting), arbiter option | `aegis/coordination/` |
| Synthetic stream with hard-benign + novel templates | `aegis/simulation/attacker.py` |

## Important limitations (read before citing any number)
* The default backend is a **proxy, not an LLM**. Its k-curve (k=0 collapse, k≥2 recovery, online > static memory)
  is partly true by construction. It validates the pipeline; **only a `--backend gemini` run is evidence about LLMs.**
* Data is synthetic template text. Next: deepset/prompt-injections, Tensor Trust, HackAPrompt, InjecAgent, AgentDojo
  (LLM threats); CIC-IDS2017 / UNSW-NB15 (network agent).
* The attacker is not adaptive yet.
* The old README's "Precision 0.91 …" numbers were not produced by this code and were removed.
  Results are generated into `results/` (CSV/JSON/PNG, mean ± 95% CI over seeds).

## Findings so far (synthetic data, simulated-LLM proxy, 20 seeds)
* The cascade's weak point was an overconfident cheap agent (Naive Bayes sure-but-wrong on novel inputs) ending
  escalation before the LLM ran. Online *calibration alone* barely helped; a cheap **novelty signal** (unseen-trigram
  share lowering ML confidence) did: F1 0.931 -> 0.976 at cost 8.3 -> 20.9 (all agents: 0.971 at 46).
  Cost now scales with novelty (LLM called ~36% of events at 50% novel traffic, ~79% at 100% novel).
* Adaptive black-box attacker (7 obfuscation operators, 12 queries): evasion IDS-only 0.96, ML-only 0.39,
  cascade+LLM 0.15, LLM-only 0.10. After learning from evasions, ML/cascade drop to ~0.02-0.04 on fresh base attacks --
  but the attacker's operator set is unchanged, so this is NOT robustness to new evasion techniques.
* Not yet done: real LLM, real datasets, an LLM-driven attacker, calibration of the proxy against real model behaviour.
