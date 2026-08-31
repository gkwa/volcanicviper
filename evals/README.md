# evals

Fixed test cases for the skills in this repo, so a change to a SKILL.md can be
measured instead of guessed at.

One file per case. The front matter holds the expected answer, the body holds
the question to ask.

The runner sends each case to `claude --print`, reads the VERDICT line off the
end of the reply, compares it to the front matter, and appends a row per trial
to the skill's `results.csv`.

Because the model is not deterministic, a single run is not a result. Use
`--repeat` and read the pass rate. A case that passes four times out of five is
telling you something a single green run would hide.

Evals live here rather than inside `skills/<name>/` so that what gets deployed
to `~/.agents/skills` stays just the SKILL.md.

## Layout

- `runner/` — the shared harness, see its own README for invocations
- `<skill-name>/cases/*.md` — one file per case
- `<skill-name>/results.csv` — every trial ever run, committed, so the diff
  shows a score moving
