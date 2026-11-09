# Provenance: when each prediction and result was committed

The experiments ran in a private repository. This is its full commit log: abbreviated hash, commit time (US Eastern, UTC-5) and message, newest first. The report (Appendix B) and `predictions.md` cite these hashes. Each prediction's commit comes before the commit of its outcome, and the private repository can be shown to reviewers to verify the hashes.

```
9a4eca4  2026-11-09 03:19  Report: public repo link on the title page; Appendix B states what is public and what is on request
19c31c6  2026-11-09 03:10  Submission copy of the final PDF and the plain-text abstract
a5e9b38  2026-11-09 03:03  README: public-facing summary, results at a glance, reproduction, safety notes
d85888c  2026-11-09 03:02  Report polish: abstract leads with the findings, checkpoints at Results and Discussion, figures redrawn narrower
d27d751  2026-11-09 02:51  Report final: consequence result (23/23 lying swarms flagged within an hour), abstract 247 words, main text ends p. 8
6962e9c  2026-11-09 02:50  CONSEQUENCE outcome: when 'yes' costs access, DeepSeek mostly stops and the rest lie; the collision test flags all 9 lying swarms within an hour
60098f2  2026-11-09 02:39  Pre-register CONSEQUENCE: the hub declines access on a yes answer (default-off switch, test, configs)
509b1a4  2026-11-09 02:30  Report: judges' presentation fixes (run table, caveats beside headlines, no line-count rhetoric), neutral-brief and adaptive-attacker results; STE variant kept for the record
c362bb5  2026-11-09 02:25  NEUTRAL outcome: without the test framing 14/15 swarms still confess; the one unprompted liar is flagged by the collision test
f509f72  2026-11-09 02:20  COV outcome: one shared decoy breaks the greedy collision test (post hoc, 0/12); a coverage test still catches it (11-12/12) but false-alarms more
fcaaa84  2026-11-09 02:14  Pre-register COV: an adaptive decoy attacker against the collision test, and a coverage-based test
4580d64  2026-11-09 02:13  Pre-register NEUTRAL: asking without the red-team framing or honesty request (brief hash recorded)
f46d9b7  2026-11-09 02:03  Report: Appendix G (H1, failed prediction: a tie, 59.8% each); build.py --src
f3259a3  2026-11-09 01:49  Report layout: Figure 2 after its section's text, appendices flow together (12 pages)
ea870d7  2026-11-09 01:47  Report: chosen title, fact-check fixes (one honest alarm at 1 h, 13/13 lying swarms, 12-15 accounts, registration wording), build asserts numbers
12cce50  2026-11-09 01:25  Final report draft: ask, then count collisions (NeurIPS-style HTML, built to PDF with numbers read from results)
42a940b  2026-11-09 01:22  ASK and DENY outcomes: 221/222 uncoached answers disclose; told to deny, every lying swarm is flagged within an hour
dfefe60  2026-11-09 00:58  EV outcome: the collision test catches 9/10 of the slow swarms that beat A and C3; deniability costs 2.7-4.3x
86fdc14  2026-11-09 00:57  Pre-register DENY: the operator tells its agents to answer no (brief hash recorded; attacker-side files untracked)
e1f7155  2026-11-09 00:51  Pre-register EV: the collision test (a denial vs the downloads), plus the ASK scorer and batch driver
c90ee36  2026-11-09 00:42  Pre-register ASK: one question on the gated access form, with a sham control
ee64a14  2026-11-08 21:37  R3b: the cheapest evasion is ~3 accounts/hour (1.3 min -> ~3 h)
c0b0fc8  2026-11-08 21:34  Pre-register R3b: the cheapest evasion (batches of K per hour), correct R3
f532092  2026-11-08 21:29  R5: out-of-sample partition cutoffs and A's recall at its cutoff
f62a4a3  2026-11-08 21:28  R4: true null on 24 fresh honest-only worlds (seeds 401-424)
49dd8c0  2026-11-08 20:38  R2 live scoring of A and C3; R3 evasion price by time-stretch replay
8c65b37  2026-11-08 20:11  R1: eval/score.py on all 39 attack runs (replaces hand recounts)
e269984  2026-11-08 20:01  Pre-register the panel's free checks R1-R5 before generating seeds 401-424
2640ea9  2026-11-08 17:14  Journal: real-swarm arm built, pre-registered and confirmed
dbfa22f  2026-11-08 17:14  Real-swarm arm (one network per account): primary CONFIRMED
55d2bb3  2026-11-08 15:45  Real-swarm arm: default-off per-account origins + pre-registration
7f12c5e  2026-11-08 15:27  Journal: afternoon block (DeepSeek confirmed, older Claude swarms, any-two closed)
f739d5c  2026-11-08 15:26  DeepSeek fresh seeds 171-179: primary CONFIRMED (second model family)
f9500d5  2026-11-08 15:05  Commit any-two recalibration + its check (ties at the cutoff, A1 split)
d858cc0  2026-11-08 14:36  Older Claude models: prediction FAILED, both build swarms (exploratory)
7d5ae91  2026-11-08 14:05  Batch scorer for any model family + clarify the weights-draw pivot case
b786476  2026-11-08 13:58  Pre-register frozen-brief runs on Claude Opus 4.8 and Sonnet 4.6
d0d41b2  2026-11-08 13:56  Pre-register DeepSeek-flash fresh-seed batch (171-179) before generating it
0ccdd24  2026-11-08 13:52  Add DeepSeek API provider for the swarm harness (DeepSeek agent's work)
3ef743f  2026-11-08 11:27  Journal heartbeat: recalibration in flight; 5.5 first panel 9.4/15 noted
f864d67  2026-11-08 11:25  Label h4.json as the pooled whole-run recalibration baseline (not H4/F01)
9b1a10a  2026-11-08 11:23  Add results/h4.json: H4 two-plane vs any-two baseline (F01), faithful replay
c0d285d  2026-11-08 11:23  Journal: Table 3 grid expanded; judge-(c) recalibration launched
67a50a3  2026-11-08 11:22  Recalibration script: calibrate on A0cal only; report held-out + A1 + swarm (5.5)
b90f896  2026-11-08 11:21  Table 3: full p_same grid (G1/G3/G4, all detectors) + 5.5 confirms
9cb8061  2026-11-08 11:16  Journal: F32-F34 Table 3 done; judge ask (c) baseline running
198e1f8  2026-11-08 11:16  Add any-two recalibration script for judge ask (c) (ready to run)
a129a22  2026-11-08 11:13  F32-F34 Table 3 regen: real declarations + C3 column (results/table3_detectors.json)
8fb1825  2026-11-08 11:02  Journal: 5.5 correction batch + G4 + judge ask (b) complete
60664db  2026-11-08 11:01  G4 result: just-minted declared lab passes C3, paged by H7 (sham-org hole)
b60b59f  2026-11-08 11:00  Pre-register G4 just-minted declared lab (sham-org-hole fixture) before scoring
0f05640  2026-11-08 10:58  Apply 5.5 corrections: v1 measured, known-answer caveats, elicitation taxonomy
15ab80e  2026-11-08 10:54  Journal: judge asks (a) done + elicitation done; (b) 301 done, 302 in flight
00d47d1  2026-11-08 10:53  Add results/a2a_elicitation.json (backs F15/F16/F40-F43, full tally)
19c59dc  2026-11-08 10:46  Judge ask (a): C3 challenges a honest divider formed AFTER the warm-up
f75315b  2026-11-08 10:45  Fix honesttwin_gen3 declared control: real orgs.jsonl + access path
2fd9b1a  2026-11-08 10:41  Pre-register honest-twin-after-warmup (judge ask a) before scoring
6f5ac2e  2026-11-08 10:39  pertick_c3 nit (5.5): evaluate challenge-warmup at first tick >= 7d (day 7.0)
f484d3c  2026-11-08 10:35  Journal: journal-only results JSONs F23 + F04 done; scope-check rest with 5.5
5a410a6  2026-11-08 10:34  Add results/v1_honest_zero.json (backs F04: the honest zero is impact-plane)
1ee2aa1  2026-11-08 10:33  Add results/h7_calibration.json (backs F23: H7 two-plane census)
45dd0e7  2026-11-08 10:29  Journal: C3 per-tick keystone qualified (thin test + history gate)
b717e68  2026-11-08 10:28  C3 per-tick: qualify the honest "0" -- thin test + permanent week-1 exemption
6610bb6  2026-11-08 10:23  Journal: C3 per-tick exemption look-ahead fixed (verified doesn't bite)
d2e795a  2026-11-08 10:23  C3 per-tick: fix exemption-lookahead justification + add account units (5.5)
b8d5d9f  2026-11-08 10:17  Journal: per-tick H7 triple-verified + C3 keystone holds causally
a10a074  2026-11-08 10:16  C3-partition per-tick: keystone "no honest group" HOLDS causally
1d2f8ed  2026-11-08 10:11  Pre-register C3-partition per-tick (T55-19 part 2) before scoring
ccf088f  2026-11-08 10:08  Per-tick H7: add persistence + offset medians; triple-verified with 5.5
e714b31  2026-11-08 10:03  Journal: per-tick H7 corrected (5.5 caught streaming-vs-tick bug)
56a59cf  2026-11-08 10:02  Corrected per-tick H7 result (tick-boundary): honest false pages 5 -> 2
291b48f  2026-11-08 09:58  Fix per-tick scorer to TRUE tick-boundary eval (5.5 caught 2 bugs)
94e1019  2026-11-08 09:54  Journal: per-tick H7 first-pass + 5 morning-summary fixes logged
7b44b76  2026-11-08 09:53  Per-tick H7 re-score (first-pass): forensic gap + causal honest false pages
22789c5  2026-11-08 09:49  Pre-register per-tick (causal) re-score of H7 (T55-19) before scoring
deb6f2f  2026-11-08 09:44  Morning summary: 5 integrity fixes (5.5 verify)
dd613bc  2026-11-08 09:34  C3 label fix: 136-145 is pre-existing for C3, not prospective (5.5)
f8aa829  2026-11-08 09:33  C3 traceability: complete c3_partition_swarm (16/16) + warm-up caveat
fda89e7  2026-11-08 09:17  Journal + morning summary: C3 confirmatory folded in; agenda complete, idling
11d0997  2026-11-08 09:13  C3 confirmatory result (fixed rule on fresh post-commit seeds)
75815d9  2026-11-08 08:38  Pre-register C3 confirmatory: fixed rule (c3_score_v3) before fresh seeds
eab5c88  2026-11-08 08:26  Correct C3 access-form honest cost to the pre-registered-rule primary (53-124/run)
d41e4b3  2026-11-08 08:22  Fold in corrected C3 re-score: exemption FAILED (post-hoc fix exploratory); access-form honest cost ~78/run
446c4f5  2026-11-08 08:13  Lock C3 integrity framing: pre-registered exemption FAILED stays failed; re-score is post-hoc
4652885  2026-11-08 08:11  Flag C3 under correction (5.5): FAILED exemption prediction, per-run units, cold-start
cc8847f  2026-11-08 07:23  Surface 3 report decisions for the user (incl. DeepSeek disclosure vs SAFETY.md); agenda complete
54231f0  2026-11-08 07:13  C3 prospective wording (5.5): n=2 Wilson CI; 152/154/155 unreachable not no-attack
2c704e5  2026-11-08 07:11  Correct two harness defects (5.5): weights-tool-defect + credential isolation
190ed86  2026-11-08 07:08  Genuinely-prospective C3 confirmation (new post-pre-reg seeds)
eb05fed  2026-11-08 06:48  C3 labelling fix (5.5): pre-registered-before-scoring, not prospective
e33793b  2026-11-08 06:45  C3 follow-up: prospective 136-145 confirmed; honest fresh/dev split
c1d7038  2026-11-08 06:43  Correct overclaim: C1 envelope does NOT close the sham-org hole (5.5)
e896a54  2026-11-08 06:41  Morning-summary: C3 friction confirmatory -> Settled; only DeepSeek arm pending
b390c99  2026-11-08 06:40  C3 friction layer measured (confirmatory): the thesis made measurable
aac299f  2026-11-08 06:33  Timestamp correction: estimated EST labels ~2h fast; git times are authoritative
e6c0813  2026-11-08 06:31  Pre-register C3 friction parameters + predictions before the fork scores
4656e1c  2026-11-08 06:31  Heartbeat 18: C3 spec locked (5.5 §4.1); constrained fork scoring both variants
fe6470c  2026-11-08 06:27  Sharpen thesis in morning-summary: friction must land at identity, not per-account quota
bb93503  2026-11-08 06:27  Heartbeat 17: C3 prototype sharpens the thesis (friction must be at identity)
9db7476  2026-11-08 06:23  Heartbeat 16: add C3 friction column to the frontier (5.5); scope "combined"
c2f01c3  2026-11-08 05:54  Heartbeat 15: pre-register cost-of-evasion frontier predictions; re-nudge DeepSeek
7366bf8  2026-11-08 05:26  Fix 4 contradictions in morning-summary (per 5.5 review)
903b2e8  2026-11-08 05:24  Refresh morning-summary: evasion-arm status + 5.5 §3 fix proposals
1a29d81  2026-11-08 05:23  Heartbeat 14: correct journey §11 separator claim; log 5.5 §3 proposals
e190801  2026-11-08 04:54  Heartbeat 13: evasion arms too weak on Haiku; org tool works; need Gemini re-run
780f48f  2026-11-08 04:51  Heartbeat 12: morning summary; flag config hygiene; note runaway-fork duplication
f942a73  2026-11-08 04:46  Heartbeat 10: natural evade rate 0% (pre-registered, prospective) — confirmed
af38c12  2026-11-08 04:44  Heartbeat 9: fresh out-of-sample honest weeks (303-305) -> 0 union false pages
07db7e9  2026-11-08 04:43  Heartbeat 11: natural H7 evade rate = 0% (prospective 7/7, combined 12/12)
dbb3fbd  2026-11-08 04:35  Heartbeat 10: fresh-honest-weeks union FP = 0/3 (out-of-sample), separators non-vacuous
8bc4af7  2026-11-08 04:00  Heartbeat 8: pre-registration timing split + 5.5 review corrections + user flag
1e8ce22  2026-11-08 03:53  Pre-register prospective H7 evade-rate test (seeds 131-145) before results land
800ebd3  2026-11-08 03:40  Fix results/h7_heldout.json: accurate completed-vs-attack counts + caveats
2ba27f4  2026-11-08 03:35  Heartbeat 5: multi-model matrix — headline generalizes to Gemini family
5b4984c  2026-11-08 03:24  Heartbeat 4: approve evasive harness hooks (new module); log TASK 001 finding
bf79382  2026-11-08 03:10  Heartbeat 3: G4 fresh-declared-lab control confirms the provenance fix direction
5d11814  2026-11-08 03:02  Heartbeat 2: preserve prototypes; fold in Fork 1 (B-fix + conditioned honest-twin)
9f05dbc  2026-11-08 02:57  Pre-register TASK 002 (sham-org) predictions + mandatory fresh-declared-lab control
ee96729  2026-11-08 02:55  Heartbeat 1: fix remaining journey overclaims (timing, §9 wording, post-hoc labels)
48c7f07  2026-11-08 02:52  Queue DeepSeek TASK 002: sham-org-declaring swarm (tests Hole 1)
a70b59b  2026-11-08 02:39  DeepSeek two-way channel + poller; fold in Tier-0 fork findings
974d599  2026-11-08 02:33  Set up overnight autonomous iteration: journal, ledger, coordination, T021
0bc74c9  2026-11-08 02:28  Correct overclaims flagged by the Opus-5.5 red-team review
1ec1ab3  2026-11-08 02:15  Add BYO-AI future-direction (identity friction as a business model)
1dcabf3  2026-11-08 01:46  Validate two origin-independent detectors on held-out; synthesise v2
fbf7e99  2026-11-08 01:36  Record held-out H7 result: v1 misses 9/9 swarms, H7 catches 7/7 completed
d4519c0  2026-11-08 01:22  Pre-register H7 (co-registration + partition) and record the H0 v1 negative
78c54ee  2026-11-08 00:57  Lock the code + thresholds that produced the results
2a9272c  2026-11-08 00:48  Lock pre-registration, design, and measured results before final build
```
