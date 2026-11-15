"""Self-healing monitor for userafael.com (Rafael landing site). Standard library only.

Based on the self-healing-monitor template. Checks:
- checks.json "checks": plain URL checks (status + text).
- "optional_https": HTTPS is only a warning while it is not set up yet; once it answers, the
  certificate must have 10+ days left.
- "pages": GitHub Pages build status for this repo. Safe auto-fix: re-request a Pages build
  when the latest build errored.
- "release_apk": the newest non-draft release of the Android repo (pre-releases included) must
  have a Rafael-v*.apk asset that downloads (ranged GET of 1 byte, so nothing big is fetched).
Uses only the workflow's GITHUB_TOKEN. Opens/closes `monitor` issues; never deletes anything.
"""
from __future__ import annotations

import concurrent.futures as cf
import datetime as dt
import json
import os
import socket
import ssl
import time

from guardian_core import with_backoff
from monitor_lib import Result, gh, http, load_state, now_iso, save_state, sync_issues, write_summary

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = json.load(open(os.path.join(HERE, "checks.json"), encoding="utf-8"))
state = load_state()


def one(c: dict) -> Result:
    """URL check with exponential backoff (2 s, 4 s, 8 s between tries)."""
    expect, timeout = int(c.get("expect", 200)), float(c.get("timeout", 20))

    def call():
        status, body, err = http(c["url"], method=c.get("method", "GET"), timeout=timeout, retries=0)
        return status, err, status == expect and (not c.get("contains") or c["contains"].encode() in body)

    (status, err, good), tries = with_backoff(call, lambda r: r[2], tries=int(c.get("tries", 4)))
    note = f" after {tries} tries" if tries > 1 else ""
    detail = f"{status}{note}" if good else f"answered {status or err} (expected {expect}{' with the page text' if c.get('contains') else ''}){note}"
    return Result(c["name"], good, detail)


def cert_days(host: str) -> int:
    with socket.create_connection((host, 443), timeout=10) as sock, \
            ssl.create_default_context().wrap_socket(sock, server_hostname=host) as s:
        end = dt.datetime.strptime(s.getpeercert()["notAfter"], "%b %d %H:%M:%S %Y %Z").replace(tzinfo=dt.timezone.utc)
    return (end - dt.datetime.now(dt.timezone.utc)).days


def optional_https(c: dict) -> Result:
    try:
        days = cert_days(c["host"])
    except Exception as e:  # noqa: BLE001 - no certificate yet is expected for now
        return Result(c["name"], True, f"not available yet ({type(e).__name__}); warning only", warn=True)
    if days < 10:
        return Result(c["name"], False, f"certificate has only {days} days left")
    r = one(c)
    if r.ok:
        r.detail = f"200, certificate {days} days left"
    return r


def pages(c: dict) -> Result:
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    if not repo or not os.environ.get("GITHUB_TOKEN"):
        return Result(c["name"], True, "skipped (no GitHub token)", warn=True)
    s, info = gh("GET", f"/repos/{repo}/pages")
    if s != 200 or not isinstance(info, dict):
        return Result(c["name"], False, f"Pages API answered {s}")
    s, build = gh("GET", f"/repos/{repo}/pages/builds/latest")
    bstatus = build.get("status") if isinstance(build, dict) else None
    if s == 200 and bstatus in ("built", "building", "queued"):
        note = "" if info.get("https_enforced") else "; HTTPS not enforced yet"
        return Result(c["name"], True, f"latest build {bstatus}{note}", warn=bool(note))
    r = Result(c["name"], False, f"latest build status {bstatus or s}")
    if c.get("rebuild_on_error") and not os.environ.get("GUARDIAN_DRY_RUN"):
        rs, _ = gh("POST", f"/repos/{repo}/pages/builds")
        r.fixes.append(f"re-requested a Pages build ({rs})")
    return r


def release_apk(c: dict) -> Result:
    s, rels = gh("GET", f"/repos/{c['repo']}/releases?per_page=10")
    if s != 200 or not isinstance(rels, list):
        return Result(c["name"], False, f"releases API answered {s}")
    for rel in rels:
        if rel.get("draft"):
            continue
        assets = [a for a in rel.get("assets", [])
                  if a.get("name", "").startswith(c["asset_prefix"]) and a["name"].endswith(c["asset_suffix"])]
        if not assets:
            return Result(c["name"], False, f"{rel.get('tag_name')} has no {c['asset_prefix']}*{c['asset_suffix']} asset")
        a = assets[0]
        st, _, err = http(a["browser_download_url"], headers={"Range": "bytes=0-0"}, timeout=30)
        ok = st in (200, 206)
        return Result(c["name"], ok, f"{a['name']} ({rel.get('tag_name')}) answered {st or err}")
    return Result(c["name"], False, "no published release found")


def apk_configs() -> list[dict]:
    c = CONFIG.get("release_apk") or []
    return c if isinstance(c, list) else [c]


def main() -> int:
    jobs = [(one, c) for c in CONFIG.get("checks", [])] + [(optional_https, c) for c in CONFIG.get("optional_https", [])]
    if CONFIG.get("pages"):
        jobs.append((pages, CONFIG["pages"]))
    jobs += [(release_apk, c) for c in apk_configs()]
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(lambda j: j[0](j[1]), jobs))
    actions = sync_issues(results)
    state["last_run"] = now_iso()
    save_state(state)
    write_summary(results, actions)
    return 0  # failures are reported through `monitor` issues, as in the template


if __name__ == "__main__":
    raise SystemExit(main())
