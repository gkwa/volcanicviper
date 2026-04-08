---
name: return-early-pattern
description: Apply the return early pattern with guard clauses to reduce nesting and improve readability. Use when refactoring conditional logic or writing new functions with precondition checks.
---

Use guard clauses to handle edge cases and failure conditions at the top of a function. Return immediately rather than nesting the happy path inside conditionals.

Good:
```
function process(data):
    if data is null: return
    if not data.is_valid(): return
    return do_work(data)
```

Bad:
```
function process(data):
    if data is not null:
        if data.is_valid():
            return do_work(data)
```

Apply this pattern where it genuinely makes the code cleaner — functions with clear precondition checks (null references, invalid parameters, boundary conditions) followed by main business logic as the happy path.

Only apply where it reduces complexity. Preserve simple if/else structures where they are already clear. Do not force the pattern into short functions where a single if/else is more readable, or when conditions represent legitimate alternative behaviors rather than failure cases.

References:
- https://en.wikipedia.org/wiki/Guard_(computer_science)
- https://medium.com/swlh/return-early-pattern-3d18a41bba8
