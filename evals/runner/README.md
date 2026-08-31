# evalrunner

Runs a directory of skill eval cases through the Claude CLI, scores each verdict
against the case's expected answer, and appends the run to a results CSV.

<!-- run every case once -->
```
uv run --no-active --project /Users/mtm/pdev/taylormonacelli/volcanicviper/evals/runner evalrunner --cases /Users/mtm/pdev/taylormonacelli/volcanicviper/evals/thesourdoughjourney-method-check/cases --results /Users/mtm/pdev/taylormonacelli/volcanicviper/evals/thesourdoughjourney-method-check/results.csv
```

<!-- run every case five times, because one sample of a stochastic system means nothing -->
```
uv run --no-active --project /Users/mtm/pdev/taylormonacelli/volcanicviper/evals/runner evalrunner --cases /Users/mtm/pdev/taylormonacelli/volcanicviper/evals/thesourdoughjourney-method-check/cases --results /Users/mtm/pdev/taylormonacelli/volcanicviper/evals/thesourdoughjourney-method-check/results.csv --repeat 5
```
