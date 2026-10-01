<<<<<<< HEAD
# Aegis-AI — Resource-Aware, Fault-Tolerant Multi-Agent Cyber Defense (research prototype)

Cheapest-first **cascade** of specialised agents (IDS → ML → AI-heuristic → few-shot LLM) under a
per-event **budget**, with Beta-Bernoulli **trust** weighting and an LLM agent that learns from
**2–5 retrieved examples** plus an online example memory.

## Run
    pip install -r requirements.txt
    python main.py --n 300 --k 3                 # one run (offline simulated-LLM backend)
    python -m experiments.run_experiments --seeds 20 --n 300
    python -m unittest discover -s tests -t .    # 13 tests
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
=======

🛡️ Aegis-AI

Adaptive Multi-Agent Cyber Defense Framework for AI-Driven Threats

---

🔬 Overview

Aegis-AI is a research-oriented cybersecurity framework that models adaptive, multi-agent defense mechanisms against both traditional and AI-driven cyber threats.

The system integrates:

- Rule-based detection (IDS)
- Machine learning anomaly detection
- AI-based semantic reasoning
- LLM-powered adversarial analysis
- Trust-aware multi-agent coordination

Unlike conventional systems, Aegis-AI is designed around the principle:

«“AI must defend against AI—not just assist traditional security.”»

---

🧠 Research Motivation

Modern cyber threats are rapidly evolving toward AI-driven automation, including:

- Prompt injection attacks
- Adversarial inputs
- Autonomous malware generation
- Social engineering at scale

Existing defenses treat AI as a tool.
Aegis-AI reframes the problem:

«Cybersecurity as a distributed, intelligent, adaptive system of cooperating agents.»

---

🏗️ System Architecture

The framework is structured as a layered, modular system:

Threat Input
    ↓
Multi-Agent Layer
    ├── IDS Agent (signature-based)
    ├── ML Agent (anomaly detection)
    ├── AI Agent (heuristic reasoning)
    └── LLM Agent (semantic threat analysis)
    ↓
Communication Layer (Message Bus)
    ↓
Trust Model (dynamic agent weighting)
    ↓
Coordinator (decision aggregation)
    ↓
Final Decision (BLOCK / MONITOR / ALLOW)

---

🤖 Multi-Agent Design

Each agent operates independently but collaborates through shared context.

Agents:

Agent| Role
IDS Agent| Fast detection of known threats
ML Agent| Statistical anomaly detection
AI Agent| Rule-based reasoning
LLM Agent| Semantic + adversarial analysis

---

📡 Communication Layer

Aegis-AI implements a lightweight Message Bus enabling:

- Alert broadcasting
- Shared threat awareness
- Cross-agent influence
- Context-aware decision-making

This transforms the system from:

- Independent agents ❌
  to
- Collaborative intelligence ✔

---

🔐 Trust Model

Each agent is assigned a dynamic trust score:

- Updated based on correctness
- Influences decision weight
- Enables adaptive reliability

This introduces:

«Trust-aware decision-making in distributed AI security systems»

---

🧠 LLM Security Layer

The LLM Agent provides:

- Prompt injection detection
- Malicious instruction analysis
- Semantic threat reasoning
- AI-vs-AI defense capability

Supports:

- Gemini API (default)
- Fallback rule-based mode (offline)

---

⚙️ Core Features

- Multi-agent coordination
- Trust-aware aggregation
- Adaptive escalation
- Resource-aware execution
- AI-driven threat detection
- Modular research architecture

---

🧪 Experimental Framework

The project includes a dedicated experiments pipeline:

Experiments:

- With LLM vs Without LLM
- Trust evolution over time
- Detection performance

Metrics:

- Precision
- Recall
- Accuracy
- F1-score

Output:

- Performance comparison
- Graph visualizations
- Trust adaptation logs

---

📊 Example Experiment Output

Precision: 0.91
Recall: 0.87
Accuracy: 0.89
F1-score: 0.89

---

🚀 Getting Started

1. Clone the repository

git clone https://github.com/Ahmed-Gomaa-Mo-CS/aegis-ai.git
cd aegis-ai

---

2. Install dependencies

pip install -r requirements.txt

---

3. Configure API key (optional)

Create ".env" in project root:

GEMINI_API_KEY=your_api_key_here

---

4. Run system

python main.py

---

5. Run experiments

python experiments/run_experiments.py

---

📁 Project Structure

aegis-ai/
│
├── aegis/                  # Core system
│   ├── agents/
│   ├── coordination/
│   ├── core/
│   └── evaluation/
│
├── experiments/            # Research experiments
│
├── main.py                 # System entry point
├── requirements.txt
└── README.md

---

🔍 Research Contributions

This project explores:

- Multi-agent cybersecurity systems
- Trust-aware AI coordination
- LLM-based threat reasoning
- AI-driven attack defense
- Distributed security architectures

---

📌 Research Direction

Aegis-AI is an early-stage implementation of a broader research agenda:

«Building autonomous, self-expanding cybersecurity systems capable of defending against intelligent adversaries.»

Future work includes:

- Distributed agent networks (blockchain-based identity)
- Real-world datasets integration
- LLM fine-tuning for security tasks
- Graph-based threat propagation
- Zero-day attack simulation

---

🎓 Academic Context

This project is developed as part of a research trajectory toward:

- PhD in Computer Science
- Cybersecurity + AI specialization
- Autonomous defense systems

---

⚠️ Disclaimer

This is a research prototype intended for experimentation and academic exploration.
It is not a production-ready security system.

---

📬 Contact

Ahmed Gomaa Mohammed
Computer Science (Cybersecurity & AI)

GitHub:
https://github.com/Ahmed-Gomaa-Mo-CS

—
>>>>>>> 1a004f91eda03eafd4e26b1cf9dbdc33beff3bbb
