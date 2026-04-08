---
name: txtar
description: Present multi-file code changes in txtar format as a single code block. Use when sharing or requesting code that spans multiple files.
---

Show code as txtar format in a single code block.

The txtar format is a single text file containing one or more file headers:

```
-- filename --
```

The file contents go directly beneath the header. There is no whitespace before or after the `--` delimiters.

Example — `file1.txt` contains `a` and `src/file2.c` contains `int i=0;`:

```
-- file1.txt --
a
-- src/file2.c --
int i=0;
```

Rules for responses using txtar:

- Only include files that have changed, not all files.
- When a file changes, include the entire file — do not abbreviate with comments like `// ... rest of the file remains unchanged ...`.
- Keep all file changes in a single txtar block. Do not split across multiple blocks with commentary in between.
