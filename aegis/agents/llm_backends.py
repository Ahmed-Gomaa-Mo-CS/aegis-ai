"""LLM backends. Both return the raw model text (expected: a JSON object)."""
import json
import logging
import os
import random
import re

from .base_agent import AgentError

log = logging.getLogger(__name__)


class GeminiBackend:
    """Real model via the `google-genai` SDK (pip install google-genai).
    NOTE: written against the public SDK docs but not executed in the
    offline environment where this refactor was produced -- test it first."""

    def __init__(self, model=None, timeout_s=15, retries=1):
        try:
            from google import genai
            from google.genai import types
        except ImportError as e:
            raise AgentError("google-genai not installed") from e
        key = os.getenv("GEMINI_API_KEY")
        if not key:
            raise AgentError("GEMINI_API_KEY is not set")
        self._types = types
        self._client = genai.Client(api_key=key, http_options=types.HttpOptions(timeout=timeout_s * 1000))
        self.model = model or os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        self.retries = retries

    def generate(self, req):
        cfg = self._types.GenerateContentConfig(
            system_instruction=req["system"], temperature=0.0,
            response_mime_type="application/json")
        last = None
        for attempt in range(self.retries + 1):
            try:
                resp = self._client.models.generate_content(
                    model=self.model, contents=req["prompt"], config=cfg)
                return resp.text or ""
            except Exception as e:  # SDK raises various error types
                last = e
                log.warning("Gemini call failed (attempt %d): %s", attempt + 1, e)
        raise AgentError(f"Gemini unavailable: {last}")


class SimulatedLLMBackend:
    """OFFLINE PROXY, not a language model.

    Behaves like a weak zero-shot prior plus similarity-weighted voting over the
    in-context examples it is shown. Purpose: exercise the full pipeline
    (retrieval -> prompt -> JSON -> parsing -> cascade -> trust) and make the
    k-shot / budget / fault-tolerance experiments runnable without an API key.
    Its k-curve is a property of this proxy, NOT evidence about real LLMs.
    """

    def __init__(self, seed=0, failure_rate=0.0):
        self.rng = random.Random(seed)
        self.failure_rate = failure_rate

    def generate(self, req):
        if self.rng.random() < self.failure_rate:
            raise AgentError("simulated LLM outage")
        payload = req["payload"].lower()
        prior = 0.35 if re.search(r"ignore (all )?(previous|prior)", payload) else 0.0
        exs = req["examples"]
        if exs:
            w = [e["sim"] ** 2 for e in exs]
            votes = sum(wi * (1 if e["label"] == "block" else -1) for wi, e in zip(w, exs)) / (sum(w) or 1)
        else:
            votes = 0.0
        sig = [1 if s["decision"] == "block" else -1 if s["decision"] == "safe" else 0
               for s in req["signals"]]
        ctx = 0.05 * (sum(sig) / len(sig)) if sig else 0.0
        p = min(1.0, max(0.0, 0.5 + prior + 0.45 * votes + ctx + self.rng.gauss(0, 0.04)))
        if p > 0.7:
            out = {"decision": "block", "confidence": round(p, 2)}
        elif p > 0.45:
            out = {"decision": "suspicious", "confidence": round(0.5 + abs(p - 0.5), 2)}
        else:
            out = {"decision": "safe", "confidence": round(1 - p, 2)}
        out["reason"] = "simulated"
        return json.dumps(out)


def make_backend(name, seed=0, failure_rate=0.0):
    if name == "gemini":
        return GeminiBackend()
    if name == "sim":
        return SimulatedLLMBackend(seed=seed, failure_rate=failure_rate)
    raise ValueError(f"unknown backend: {name}")
