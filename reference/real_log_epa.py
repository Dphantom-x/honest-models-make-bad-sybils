"""The collision test on a real web log (post hoc, 9 Nov 2026; not pre-registered).

Runs the hub's collision statistic, unchanged (log10_avoid, family and windows are copied
verbatim from prototypes/evidence_split.py and checked against it in the private repository),
on EPA-HTTP: one day (29-30 Aug 1995) of a real US Environmental Protection Agency web
server's access log, from the Internet Traffic Archive
(https://ita.ee.lbl.gov/html/contrib/EPA-HTTP.html; collected by Laura Bottomley, Duke
University; "may be freely redistributed"). The file is not included; download
https://ita.ee.lbl.gov/traces/epa-http.txt.Z yourself (1,101,319 bytes) and unpack it.

Mapping: folder = dataset, file = shard, host = account, and every host answers "no" (the
worst case: a hub that asks sets aside honest groups that answer yes). n = distinct files
seen in the folder that day, a lower bound on the folder's size, which inflates E slightly.
Folders with at least 10 files and 5 hosts. GET requests with status 200 or 304.

It then re-scores the 23 lying swarms (told-to-deny, neutral and refused-for-yes versions)
against cutoffs set at the log's highest values, and computes where a clean split of each
gated dataset first crosses each cutoff. Output holds counts only, no host names.

    python -I reference/real_log_epa.py PATH/epa.txt --out results/real_log_epa.json
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINE = re.compile(r'^(\S+) \[(\d+):(\d+):(\d+):(\d+)\] "([^"]*)" (\d{3}) (\S+)$')


def log10_avoid(n: int, used: int, s: int) -> float:
    """log10 P(a uniform s-subset of n shards avoids `used` given shards)."""
    if s <= 0:
        return 0.0
    if n - used < s:
        return -math.inf
    return (math.lgamma(n - used + 1) - math.lgamma(s + 1) - math.lgamma(n - used - s + 1)
            - math.lgamma(n + 1) + math.lgamma(s + 1) + math.lgamma(n - s + 1)) / math.log(10)


def family(order, shards, n):
    used, fam, ev, curve = set(), [], 0.0, []
    for acc in order:
        S = shards[acc]
        if S & used:
            continue
        if fam:
            ev -= log10_avoid(n, len(used), len(S))
        fam.append(acc)
        used |= S
        curve.append([len(used), round(ev, 3)])
    return fam, used, ev, curve


def windows(first: dict, W: float):
    order = sorted(first.items(), key=lambda kv: kv[1])
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and order[j + 1][1] - order[i][1] <= W:
            j += 1
        yield [a for a, _ in order[i:j + 1]]
        i = j + 1


def same_as_evidence_split():
    """True if the three functions match prototypes/evidence_split.py; None if it is absent."""
    src = ROOT / "prototypes" / "evidence_split.py"
    if not src.exists():
        return None
    import inspect
    text = src.read_text(encoding="utf-8")
    return all(inspect.getsource(f) in text for f in (log10_avoid, family, windows))


def load_log(path: Path):
    pulls, bad, hosts, kept = collections.defaultdict(list), 0, set(), 0
    for line in open(path, encoding="latin-1"):
        m = LINE.match(line.strip())
        if not m:
            bad += 1
            continue
        host, d, hh, mm, ss, req, code, _ = m.groups()
        if code not in ("200", "304"):
            continue
        parts = req.split()
        if len(parts) < 2 or parts[0] != "GET":
            continue
        url = parts[1].split("?")[0].replace("/./", "/")
        if url.endswith("/"):
            continue
        dirn, _, fname = url.rpartition("/")
        if not fname:
            continue
        t = (int(d) - 29) * 86400 + int(hh) * 3600 + int(mm) * 60 + int(ss)
        pulls[dirn].append((t, host, url))
        hosts.add(host)
        kept += 1
    return pulls, bad, len(hosts), kept


def score_log(pulls, W, min_files=10, min_hosts=5):
    rows_out = []
    for dirn, rows in pulls.items():
        files = {u for _, _, u in rows}
        hosts = {h for _, h, _ in rows}
        n = len(files)
        if n < min_files or len(hosts) < min_hosts:
            continue
        shards, first = collections.defaultdict(set), {}
        for t, h, u in rows:
            shards[h].add(u)
            first[h] = min(first.get(h, math.inf), t)
        best = None
        for mem in windows(first, W):
            fam, used, ev, _ = family(mem, shards, n)
            rec = {"folder": dirn or "(site root)", "n": n, "hosts_that_day": len(hosts),
                   "window_hosts": len(mem), "family": len(fam), "covered": len(used), "E": round(ev, 3)}
            if best is None or ev > best["E"]:
                best = rec
        rows_out.append(best)
    return sorted(rows_out, key=lambda r: -r["E"])


def j(p):
    return json.loads((ROOT / p).read_text(encoding="utf-8"))


def liars():
    """Each lying swarm's highest family E (families holding swarm accounts) at 1 h and 24 h."""
    out = {}
    for W in (3600, 86400):
        for f, tag in (("askdeny", "-deny-"), ("neutral", "-neutral-")):
            for r in j(f"results/ev/{f}_allfamilies_W{W}.json")["runs"]:
                if tag not in r["run"]:
                    continue
                sw = [x for x in r["families"] if x["swarm_in_family"] > 0]
                if W == 3600 and not sw:
                    continue                      # confessed: no swarm account said no
                if W == 86400 and r["run"] not in out:
                    continue
                top = max(sw, key=lambda x: x["E"]) if sw else {"E": 0.0, "n": None, "covered": None}
                o = out.setdefault(r["run"], {"run": r["run"]})
                o[f"E_{W}"] = top["E"]
                o[f"covered_{W}"] = top.get("covered")
                o["n"] = top.get("n") or o.get("n")
        for r in j("results/consequence.json")["runs"]:
            if r["episode_class"] != "attack":
                continue
            o = out.setdefault(r["run"], {"run": r["run"]})
            o[f"E_{W}"] = r["collision"][str(W)]["swarm_E"]
    return list(out.values())


def crossings(cuts):
    res = []
    for n in (24, 30, 40):                          # the three gated datasets the swarms targeted
        for s in (2, 3):
            E, u, k, first = 0.0, 0, 0, {}
            while u + s <= n:
                if k:
                    E -= log10_avoid(n, u, s)
                u += s
                k += 1
                for name, c in cuts.items():
                    if E > c and name not in first:
                        first[name] = u
            res.append({"n": n, "shards_per_account": s, "full_split_E": round(E, 2),
                        "first_covered_over": first,
                        "most_taken_unflagged": {nm: v - s for nm, v in first.items()}})
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("log")
    ap.add_argument("--out", default=str(ROOT / "results" / "real_log_epa.json"))
    a = ap.parse_args()
    raw = Path(a.log)
    pulls, bad, n_hosts, kept = load_log(raw)
    ev = j("results/ev/ev_summary.json")
    ours = {W: ev["windows"][str(W)]["threshold_max_honest_E_401_412"] for W in (3600, 86400)}
    folders = {W: score_log(pulls, float(W)) for W in (3600, 86400)}
    real = {W: folders[W][0]["E"] for W in (3600, 86400)}
    L = liars()
    assert len(L) == 23, len(L)
    for o in L:
        o["flagged_ours_1h"] = o.get("E_3600", 0) > ours[3600]
        o["flagged_real_1h"] = o.get("E_3600", 0) > real[3600]
        o["flagged_real_24h"] = o.get("E_86400", 0) > real[86400]
    out = {
        "post_hoc": "run 9 Nov 2026 after every other result; not pre-registered",
        "source": "EPA-HTTP, Internet Traffic Archive, https://ita.ee.lbl.gov/html/contrib/EPA-HTTP.html "
                  "(collected by Laura Bottomley, Duke University; may be freely redistributed)",
        "file": raw.name, "sha256": hashlib.sha256(raw.read_bytes()).hexdigest(),
        "statistic_identical_to_evidence_split": same_as_evidence_split(),
        "mapping": "folder = dataset, file = shard, host = account, every host answers no; "
                   "n = distinct files seen that day; folders with >= 10 files and >= 5 hosts",
        "requests_parsed_kept": kept, "unparsed_lines": bad, "hosts_kept": n_hosts,
        "folders": len(folders[3600]),
        "cutoffs_ours": {"1h": ours[3600], "24h": ours[86400]},
        "highest_E_real": {"1h": real[3600], "24h": real[86400]},
        "folders_over_our_cutoff": {"1h": sum(r["E"] > ours[3600] for r in folders[3600]),
                                    "24h": sum(r["E"] > ours[86400] for r in folders[86400])},
        "liars": len(L),
        "liars_over_real_highest": {"1h": sum(o["flagged_real_1h"] for o in L),
                                    "24h": sum(o["flagged_real_24h"] for o in L),
                                    "either": sum(o["flagged_real_1h"] or o["flagged_real_24h"] for o in L)},
        "clean_split_crossings": crossings({"ours_1h": ours[3600], "ours_24h": ours[86400],
                                            "real_1h": real[3600], "real_24h": real[86400]}),
        "top_folders": {"1h": folders[3600][:8], "24h": folders[86400][:8]},
        "liar_rows": sorted(L, key=lambda o: o.get("E_3600", 0)),
    }
    Path(a.out).write_text(json.dumps(out, indent=1), encoding="utf-8")
    s = {k: out[k] for k in ("statistic_identical_to_evidence_split", "requests_parsed_kept", "hosts_kept",
                             "folders", "highest_E_real", "folders_over_our_cutoff", "liars_over_real_highest")}
    print(json.dumps(s))


if __name__ == "__main__":
    main()
