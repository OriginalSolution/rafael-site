"""Rafael Guardian: pure decision logic (no network), so it can be unit tested.

The Guardian turns one run of check results into:
- a health status: "ok" or "attention", with a plain reason;
- incident log entries (opened / resolved / repair / dispatch);
- whether to send the repository_dispatch "guardian-attention" event.
"""
from __future__ import annotations

import time
from typing import Callable, TypeVar

T = TypeVar("T")


def backoff_delays(tries: int, base: float = 2.0, cap: float = 30.0) -> list[float]:
    """Waits between tries: base, 2*base, 4*base ... capped. tries=4 -> [2, 4, 8]."""
    return [min(cap, base * (2 ** i)) for i in range(max(0, tries - 1))]


def with_backoff(fn: Callable[[], T], ok: Callable[[T], bool], tries: int = 4, base: float = 2.0,
                 sleep: Callable[[float], None] = time.sleep) -> tuple[T, int]:
    """Calls fn until ok(result) or tries run out. Returns (last result, attempts used)."""
    delays = backoff_delays(tries, base)
    result = fn()
    attempt = 1
    while not ok(result) and attempt < tries:
        sleep(delays[attempt - 1])
        result = fn()
        attempt += 1
    return result, attempt


def summarize(results: list[dict]) -> tuple[str, str]:
    """results: [{name, ok, detail}] -> (status, plain reason)."""
    bad = [r for r in results if not r["ok"]]
    if not bad:
        return "ok", "All checks passed."
    return "attention", "; ".join(f"{r['name']}: {r['detail']}" for r in bad)


def advance(state: dict, results: list[dict], now: str, attention_after: int = 2, redispatch_every: int = 4) -> dict:
    """Updates state in place and returns {status, reason, incidents, dispatch}.

    state keys: consecutive_attention, failing {check: since}, last_ok_at, last_status.
    A dispatch is sent when attention has lasted `attention_after` runs in a row, then again every
    `redispatch_every` runs while it continues (so a stuck problem is not forgotten, but not spammed).
    """
    status, reason = summarize(results)
    failing: dict = state.setdefault("failing", {})
    incidents: list[dict] = []
    for r in results:
        if not r["ok"] and r["name"] not in failing:
            failing[r["name"]] = now
            incidents.append({"at": now, "kind": "opened", "check": r["name"], "detail": r["detail"]})
        elif r["ok"] and r["name"] in failing:
            since = failing.pop(r["name"])
            incidents.append({"at": now, "kind": "resolved", "check": r["name"], "detail": f"failing since {since}"})
        for fix in r.get("fixes", []):
            incidents.append({"at": now, "kind": "repair", "check": r["name"], "detail": fix})
    # A check that vanished from the config is no longer failing.
    names = {r["name"] for r in results}
    for gone in [n for n in failing if n not in names]:
        failing.pop(gone)
    if status == "ok":
        state["consecutive_attention"] = 0
        state["last_ok_at"] = now
    else:
        state["consecutive_attention"] = int(state.get("consecutive_attention", 0)) + 1
    n = state["consecutive_attention"]
    dispatch = n >= attention_after and (n - attention_after) % max(1, redispatch_every) == 0
    if dispatch:
        incidents.append({"at": now, "kind": "dispatch", "check": "guardian",
                          "detail": f"guardian-attention after {n} runs in attention: {reason}"})
    state["last_status"] = status
    return {"status": status, "reason": reason, "incidents": incidents, "dispatch": dispatch,
            "consecutive_attention": n}


def health_doc(service: str, outcome: dict, results: list[dict], state: dict, now: str, run_url: str) -> dict:
    return {
        "service": service,
        "status": outcome["status"],
        "reason": outcome["reason"],
        "checked_at": now,
        "consecutive_attention": outcome["consecutive_attention"],
        "last_ok_at": state.get("last_ok_at"),
        "checks": [{"name": r["name"], "ok": r["ok"], "detail": r["detail"]} for r in results],
        "run": run_url,
    }
