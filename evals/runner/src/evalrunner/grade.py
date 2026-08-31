import re

VERDICT = re.compile(r"^VERDICT:\s*(over|under|none)\s*$", re.IGNORECASE | re.MULTILINE)


def verdict(output: str) -> str:
    """Pull the final VERDICT line out of a skill's reply.

    Returns "missing" when the skill never emitted one, which counts as a
    failure rather than an error: a verdict the harness cannot read is a
    verdict the user cannot act on either.
    """
    matches = VERDICT.findall(output)
    if not matches:
        return "missing"
    return matches[-1].lower()
