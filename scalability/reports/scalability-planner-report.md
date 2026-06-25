# Multi Region Edge and Scalability Planner Report

## Regions

- Bangkok Primary [ap-southeast-th / primary / review]
- Singapore Secondary [ap-southeast-1 / secondary / review]
- Tokyo Edge [ap-northeast-1 / edge / planned]
- EU Standby [eu-west-1 / standby / planned]

## Routes

- www.zeaz.dev: latency reg_bkk->reg_sgp
- api.zeaz.dev: failover reg_bkk->reg_sgp
- docs.zeaz.dev: geo reg_sgp->reg_tok

## Safety

- Planning-only.
- No infrastructure apply.
- No production routing changes.
