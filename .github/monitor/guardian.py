"""Rafael Guardian for userafael.com. Python standard library only; uses only GITHUB_TOKEN.

Each run (schedule, after every Pages deploy, or by hand):
1. runs the monitor checks (site pages, HTTPS certificate, Pages build, latest APK download),
   each with exponential backoff;
2. repairs what it safely can: re-requests a Pages build when the last one errored; if the
   newest APK fails, it checks that the last good APK still downloads and says so;
3. keeps state on the `guardian-state` branch (never on main, never the live site):
   health.json, last_good.json, state.json and an append-only incidents.jsonl;
4. opens/updates/closes `monitor` issues, one per failing check;
5. sends repository_dispatch "guardian-attention" when attention lasts 2+ runs in a row.

GUARDIAN_DRY_RUN=1 (pull requests) does the checks only: no issues, repairs, dispatch or state.
"""
from __future__ import annotations

import concurrent.futures as cf
import json
import os

import monitor as m
from guardian_core import advance, health_doc
from monitor_lib import Result, gh, http, now_iso, run_url, sync_issues, write_summary

STATE_DIR = os.environ.get("GUARDIAN_STATE_DIR", "guardian-state")
DRY = bool(os.environ.get("GUARDIAN_DRY_RUN"))
CFG = m.CONFIG.get("guardian", {})


def read(name: str, default):
    try:
        with open(os.path.join(STATE_DIR, name), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def write(name: str, data) -> None:
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(os.path.join(STATE_DIR, name), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, sort_keys=True)
        f.write("\n")


def last_good_apk(r: Result, last_good: dict) -> None:
    """Keep the last good data: if the newest APK fails, check the last one that worked."""
    good = last_good.get("apks", {}).get(r.name)
    if r.ok or not good:
        return
    st, _, err = http(good["url"], headers={"Range": "bytes=0-0"}, timeout=30)
    r.detail += (f"; last good {good['name']} still downloads" if st in (200, 206)
                 else f"; last good {good['name']} also fails ({st or err})")


def remember_apks(last_good: dict) -> None:
    apks = last_good.setdefault("apks", {})
    for c in m.apk_configs():
        s, rels = gh("GET", f"/repos/{c['repo']}/releases?per_page=10")
        rel = next((x for x in rels if not x.get("draft")), None) if s == 200 and isinstance(rels, list) else None
        for a in (rel or {}).get("assets", []):
            if a.get("name", "").startswith(c["asset_prefix"]) and a["name"].endswith(c["asset_suffix"]):
                apks[c["name"]] = {"name": a["name"], "url": a["browser_download_url"], "tag": rel.get("tag_name")}
                break


def main() -> int:
    jobs = [(m.one, c) for c in m.CONFIG.get("checks", [])] + [(m.optional_https, c) for c in m.CONFIG.get("optional_https", [])]
    if m.CONFIG.get("pages"):
        jobs.append((m.pages, m.CONFIG["pages"]))
    jobs += [(m.release_apk, c) for c in m.apk_configs()]
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        results: list[Result] = list(ex.map(lambda j: j[0](j[1]), jobs))

    last_good = read("last_good.json", {})
    apk_names = {c["name"] for c in m.apk_configs()}
    for r in results:
        if r.name in apk_names:
            last_good_apk(r, last_good)

    now = now_iso()
    rows = [{"name": r.name, "ok": r.ok, "detail": r.detail, "fixes": r.fixes} for r in results]
    state = read("state.json", {})
    outcome = advance(state, rows, now, int(CFG.get("attention_after_runs", 2)), int(CFG.get("redispatch_every_runs", 4)))
    health = health_doc(CFG.get("service", "userafael.com"), outcome, rows, state, now, run_url())
    actions: list[str] = [f"health: {outcome['status']} - {outcome['reason']}"]

    if DRY:
        actions.append("dry run: no issues, repairs, dispatch or state written")
    else:
        actions += sync_issues(results)
        if outcome["status"] == "ok":
            remember_apks(last_good)
            last_good.update(checked_at=now, checks=[{"name": r["name"], "detail": r["detail"]} for r in rows])
        if outcome["dispatch"]:
            repo = os.environ.get("GITHUB_REPOSITORY", "")
            s, _ = gh("POST", f"/repos/{repo}/dispatches", {"event_type": "guardian-attention", "client_payload": {
                "source": "guardian", "status": outcome["status"], "reason": outcome["reason"][:500],
                "consecutive_runs": outcome["consecutive_attention"], "run_url": run_url()}})
            actions.append(f"sent guardian-attention ({s})")
        write("state.json", state)
        write("health.json", health)
        write("last_good.json", last_good)
        with open(os.path.join(STATE_DIR, "incidents.jsonl"), "a", encoding="utf-8") as f:
            for i in outcome["incidents"]:
                f.write(json.dumps(i, sort_keys=True) + "\n")
    write_summary(results, actions)
    print(json.dumps(health, indent=1))
    return 0  # problems are reported through health.json, issues and the dispatch, not a red run


if __name__ == "__main__":
    raise SystemExit(main())
