import subprocess

INSTRUCTION = """Answer using the thesourdoughjourney-method-check skill.

End your reply with a single final line, exactly one of:

VERDICT: none
VERDICT: over
VERDICT: under

Use none when Tom's method applies cleanly, over when following the chart
percentage would over-ferment the dough, and under when it would under-ferment.

"""


def claude(prompt: str, timeout: int) -> str:
    result = subprocess.run(
        ["claude", "--print", INSTRUCTION + prompt],
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())
    return result.stdout
