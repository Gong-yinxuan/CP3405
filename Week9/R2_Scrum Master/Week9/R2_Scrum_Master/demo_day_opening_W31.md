# R2 Demo Day Opening — Two-Minute Version

Good morning. I am Jinsong Jiang, presenting the Scrum Master role.

Across nine sprints, our team moved from manually written market evidence into PRISM, a structured market-intelligence pipeline. The system connects Almanac, Macro and Technical agents to multi-LLM synthesis, Human Score, automated data collection, release management and calibration.

The important evidence is not one successful prediction. Our evidence is the complete delivery chain: role files committed in order, scheduled GitHub Actions runs, saved model outputs, a working fallback when one provider failed, release tags and calibration reports showing where forecasts were wrong.

As Scrum Master, my responsibility was to protect that chain. I checked each role, surfaced missing dependencies, prevented incomplete work from being treated as done, coordinated the final run-through and withheld release approval until the Definition of Done was supported by evidence.

The main process lesson is that our remaining failures were often delivery-integrity failures: stale dates, incorrect filenames, missing quality gates and inconsistent folders. Our final improvement is an automated pre-tag audit that checks every required file and blocks the release when evidence is incomplete.

I will now hand over to our Product Owner, who will confirm the final sprint goal and Definition of Done.
