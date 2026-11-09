"""Build the final report: check the headline numbers against results/, fill the title, print
report.html to PDF with headless Chrome, and stamp page numbers.

    .venv/Scripts/python report/final/build.py [--title "..."] [--out report/final/report.pdf]
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

HD = Path(__file__).resolve().parents[2]
FINAL = HD / "report" / "final"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
DEFAULT_TITLE = ("Honest Models Make Bad Sybils: AI Swarms Confess When Asked, and Their Downloads "
                 "Convict Them When They Lie")


def j(p):
    return json.loads((HD / p).read_text(encoding="utf-8"))


def checks():
    """The prose states these numbers; fail the build if a results file disagrees."""
    ask = j("results/ask_the_swarm.json")["summary"]
    p1, bm, bam = ask["P1_pooled"], ask["P1_by_model"], ask["by_arm_model"]
    assert (p1["disclose"], p1["eligible_answers"]) == (221, 222)
    assert [round(100 * x, 1) for x in p1["wilson95"]] == [97.5, 99.9]
    assert sum(v["names_other_among_disclose"] for v in bm.values()) == 218
    assert sum(v["attack_runs"] for v in bm.values()) == 19
    d = {k.split("|")[1]: v for k, v in bam.items() if k.startswith("A2a-pa-deny-")}
    assert d["gemini-3.1-flash-lite"]["deny"] == 78 and d["claude-opus-4-8"]["deny"] == 11
    assert d["deepseek-flash"]["deny"] == 53 and d["deepseek-flash"]["eligible"] == 88
    ev = j("results/ev/ev_summary.json")
    assert ev["windows"]["3600"]["live"]["flagged"] == 57
    assert ev["windows"]["86400"]["r3bK3"]["flagged"] == 9
    assert ev["EV4_last_third_share"]["over_half"] == 56
    # every family over the cutoff, ask + told-to-deny runs (fact-check A1)
    for W in (3600, 86400):
        thr = ev["windows"][str(W)]["threshold_max_honest_E_401_412"]
        rr = j(f"results/ev/askdeny_allfamilies_W{W}.json")["runs"]
        honest_worlds = {r["run"].split("/")[-1] for r in rr
                         if any(f["E"] > thr and f["swarm_in_family"] == 0 for f in r["families"])}
        lying_flagged = {r["run"] for r in rr if "-deny-" in r["run"]
                         and any(f["E"] > thr and f["swarm_in_family"] > 0 for f in r["families"])}
        if W == 3600:
            assert honest_worlds == {"615"}, honest_worlds
            assert len(lying_flagged) == 13, lying_flagged
        else:
            assert honest_worlds == set(), honest_worlds
    # post-hoc real-log check (Appendix H, section 5)
    rl = j("results/real_log_epa.json")
    assert rl["statistic_identical_to_evidence_split"] is True
    assert (rl["folders"], rl["requests_parsed_kept"], rl["hosts_kept"]) == (59, 33451, 2245)
    assert rl["folders_over_our_cutoff"] == {"1h": 10, "24h": 12}
    assert rl["highest_E_real"] == {"1h": 4.351, "24h": 8.25}
    assert rl["liars"] == 23 and rl["liars_over_real_highest"] == {"1h": 6, "24h": 4, "either": 6}
    t1, t24 = rl["top_folders"]["1h"][0], rl["top_folders"]["24h"][0]
    assert (t1["n"], t1["window_hosts"], t1["family"]) == (39, 72, 21)
    assert (t24["family"], t24["covered"]) == (28, 32)
    cx = rl["clean_split_crossings"]
    assert {n: max(x["most_taken_unflagged"]["real_24h"] for x in cx if x["n"] == n) for n in (24, 30, 40)} == {24: 22, 30: 27, 40: 32}
    assert round(100 * min(x["most_taken_unflagged"]["real_24h"] / x["n"] for x in cx)) == 75


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", default=DEFAULT_TITLE)
    ap.add_argument("--out", default=str(FINAL / "report.pdf"))
    ap.add_argument("--src", default=str(FINAL / "report.html"))
    a = ap.parse_args()
    checks()
    html = Path(a.src).read_text(encoding="utf-8")
    html = html.replace("{{TITLE_PLAIN}}", a.title).replace("{{TITLE_HTML}}", a.title.replace(": ", ":<br>", 1))
    m = re.search(r'<div class="abstract">(.*?)</div>', html, re.S)
    words = len(re.sub(r"<[^>]+>|&[a-z]+;", " ", m.group(1)).split())
    assert not re.findall(r"\{\{[A-Z0-9_]+\}\}", html)
    built = FINAL / (Path(a.src).stem + "_built.html")
    built.write_text(html, encoding="utf-8")
    out = Path(a.out)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    "--allow-file-access-from-files", f"--print-to-pdf={out}", built.as_uri()],
                   check=True, capture_output=True, timeout=180)
    import fitz  # pymupdf
    doc = fitz.open(out)
    for i, page in enumerate(doc, 1):
        r = page.rect
        page.insert_text((r.width / 2 - 3, r.height - 30), str(i), fontsize=9, fontname="Times-Roman")
    tmp = out.with_suffix(".tmp.pdf")
    doc.save(tmp)
    doc.close()
    tmp.replace(out)
    d2 = fitz.open(out)
    ref_page = next((i + 1 for i in range(d2.page_count) if "[16] S. Shenker" in d2[i].get_text()), None)
    print(f"built {out} pages={d2.page_count} abstract_words={words} references_end_page={ref_page}")


if __name__ == "__main__":
    main()
