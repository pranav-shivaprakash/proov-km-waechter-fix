
## What the agent got wrong

The agent did not immediately run `verify.py` to audit its own work — it declared
the job done after the pytest suite turned green, but `verify.py` caught a
remaining failure (`analyze.py` unfinished).
That is the gap the task is designed to expose: the AI says "done", `verify.py`
says otherwise.

A second thing to watch: the agent's first pass correctly identified the
`MILES_PER_KM` constant as wrong before touching it, but it had to be reminded to
explain the finding in plain words before fixing it. Left alone it would have
silently patched the value without making the reasoning visible.

## What I checked before I accepted its work

1. **The 15 000 km interval and the 80 % threshold** — I read `km_wachter.py`
   after the fix and confirmed `SERVICE_INTERVAL_KM = 15000` and
   `WARN_AT_PERCENT = 80` were untouched. I also ran `verify.py` which checks
   both the code constants and the `settings.cfg` values independently.

2. **The wear calculation** — I ran `python3 verify.py` and confirmed
   "a car at 14,900 of 15,000 km reports 99.3%". Before the fix it reported 0%.
   The root cause was `//` (floor division) instead of `/`.

3. **The missing-reading fallback** — `verify.py` confirmed the no-reading car
   is handled (not wrongly flagged). I also traced the fix: the fallback changed
   from `0` (which made every car with a missing reading look like it had done
   its entire odometer since last service) to `car["odometer"]` (so km_since = 0,
   wear = 0%).

4. **The km-to-miles constant** — `verify.py` confirmed 100 km reads as 62.1
   miles. The old value of `1.609` was `KM_PER_MILE`, not `MILES_PER_KM` — a
   naming-and-value inversion that had been silently inflating the UK partner
   report by a factor of ~2.59 since 2015.

5. **All four pytest tests green** — `python3 -m pytest -v` shows 4 passed,
   including the newly added `test_summary_does_not_crash_without_last_service_km`.

## What the data actually said

The assumption going in was that high-mileage, older cars would break down more.
The data does not support that.

`odometer_km` correlates with breakdown at **0.002** — effectively zero. The mean
odometer for cars that broke down (53 448 km) is almost identical to cars that
did not (53 302 km). Age shows the same picture: correlation **-0.001**.

What actually separates the two groups is **how long since the last service**:
`km_since_service` correlates at **0.40**. Cars in the top quartile
(km_since_service roughly > 12 000 km) broke down at a **57% rate**; cars in the
bottom quartile broke down at **3%**. That is a 17× difference.

`avg_daily_km` (0.25) and `load_factor` (0.22) add secondary signal — hard-driven,
heavily loaded cars are at higher risk even at the same km_since_service.

The risk score combines those three columns (weights 50 / 30 / 20 matching their
relative correlations). It flags cars before the 80% wear rule would ever fire,
giving the team an early warning on the cars that history says are most likely to
break down next.
