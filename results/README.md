# Results index

Each file holds the numbers behind one claim; the report's Table 1 maps claims to files.

| Claim in the report | File(s) |
|---|---|
| Asked once, swarms confess (19/19; 221/222 answers); neutral brief 14/15; control question; told to deny | `ask_the_swarm.json` (arms A2a-pa-ask-*, -sham-*, -neutral-*, -deny-*) |
| The hub refuses a "yes": DeepSeek mostly stops, every attacking swarm lies, all 9 flagged | `consequence.json` |
| Collision test on every family (ask and deny runs, 1 h and 24 h) | `ev/askdeny_allfamilies_W3600.json`, `ev/askdeny_allfamilies_W86400.json` |
| Collision test on the neutral runs | `ev/neutral_allfamilies_W3600.json`, `ev/neutral_allfamilies_W86400.json` |
| Cutoffs from honest-only worlds (12 calibrate, 12 test); 58 earlier episodes; slow swarms; suspicion accelerates | `ev/ev_summary.json` and the `ev/null_*`, `ev/live_*`, `ev/r3bK3_*` files |
| Price of deniability (picking like strangers) | `ev/deniability_price.json` |
| Adaptive attacker: random and shared decoys; coverage test | `ev/coverage_test.json`, `ev/coverage_test_commondecoy.json` |
| One network per account: cohort rule 0/10, split rule 10/10 | `realswarm_peraccount.json` |
| Split rule: 58/58 attack episodes; out-of-sample cutoff | `r5_recall_A.json`, `null_worlds_r4_r5.json` |
| An honest team that splits a dataset looks the same | `table3_detectors.json`, `twin_postwarmup.json` |
| Releasing accounts in batches (3, 4, 5 per hour) | `evasion_batches_K3.json`, `evasion_batches_K4.json`, `evasion_batches_K5.json` |
| Credential alarm: 0 of 37 live runs; 0 alarms in 30 unseen honest days; incident replay | `r1_eval_score.json`, `heldout_A0.json` |
| Which models build swarms or refuse | `a2a_elicitation.json`, `deepseek_heldout.json`, `claude_older_models.json` |
| H1: a served value travels with an agent's hand-offs | `h1_primary.json`, `h1_secondary.json`, `h1_cells/` |
