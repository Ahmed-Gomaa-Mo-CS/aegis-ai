import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def plot_all(results):
    # F1 vs cost (Pareto) across baselines + budget sweep
    fig, ax = plt.subplots(figsize=(6, 4))
    for sec, marker in (("baselines", "o"), ("budget", "s")):
        for name, r in results[sec]:
            ax.errorbar(r["cost"][0], r["f1"][0], yerr=r["f1"][1], fmt=marker, capsize=2)
            ax.annotate(name, (r["cost"][0], r["f1"][0]), fontsize=6, xytext=(3, 3), textcoords="offset points")
    ax.set_xlabel("mean cost per event"); ax.set_ylabel("F1 (BLOCK)")
    ax.set_title("Accuracy vs. resource cost"); fig.tight_layout()
    fig.savefig("results/pareto.png", dpi=150); plt.close(fig)

    # k-shot curve
    fig, ax = plt.subplots(figsize=(5, 3.5))
    rows = [(n, r) for n, r in results["k_sweep"] if "static" not in n]
    ks = [int(n.split("k=")[1]) for n, _ in rows]
    ax.errorbar(ks, [r["f1"][0] for _, r in rows], yerr=[r["f1"][1] for _, r in rows], marker="o", capsize=3)
    ax.set_xlabel("k (few-shot examples)"); ax.set_ylabel("F1"); ax.set_xticks(ks)
    ax.set_title("LLM agent: F1 vs k"); fig.tight_layout()
    fig.savefig("results/kshot.png", dpi=150); plt.close(fig)

    # fault tolerance
    fig, ax = plt.subplots(figsize=(5, 3.5))
    rows = results["faults"]
    ax.plot([n.split("=")[1] for n, _ in rows], [r["f1"][0] for _, r in rows], marker="o")
    ax.set_xlabel("LLM outage rate"); ax.set_ylabel("F1"); ax.set_title("Graceful degradation")
    fig.tight_layout(); fig.savefig("results/faults.png", dpi=150); plt.close(fig)
