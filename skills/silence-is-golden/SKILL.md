---
name: silence-is-golden
description: Follow the Unix rule of silence — output nothing on the happy path. Use when designing CLI tools, scripts, or any program that runs unattended.
---

The app should not output anything for the happy path, in the spirit of the Unix rule of silence.

Reference: https://www.linfo.org/rule_of_silence.html

Only produce output when something noteworthy happens — errors, warnings, or explicitly requested information. A program that is silent on success composes well with other tools and does not clutter logs or pipelines.
