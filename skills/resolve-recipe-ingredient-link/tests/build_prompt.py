import pathlib
import typing


def _strip_frontmatter(text: str) -> str:
    parts = text.split("---", 2)
    if len(parts) == 3:
        return parts[2].strip()
    return text.strip()


def _read_skill(skill_path: pathlib.Path) -> str:
    return _strip_frontmatter(skill_path.read_text())


def build_prompt(context: typing.Dict[str, typing.Any]) -> str:
    here = pathlib.Path(__file__).parent
    skill = _read_skill(here.parent / "SKILL.md")
    products = (here / "products.txt").read_text().strip()
    line = context["vars"]["line"]
    return (
        f"{skill}\n\n"
        "You are resolving one ingredient wikilink for the recipe line below.\n\n"
        "The product-tagged candidate notes are already enumerated for you. "
        "Treat the list below as the islandiguana output and do not run any "
        "command:\n\n"
        f"{products}\n\n"
        f"Recipe ingredient line:\n{line}\n\n"
        "Output contract: respond with ONLY the resolving note filename "
        "including the .md extension, for example leek.md. "
        "If the line does not determine a single match, respond with exactly "
        "ASK. Output nothing else."
    )


def build_link_prompt(context: typing.Dict[str, typing.Any]) -> str:
    here = pathlib.Path(__file__).parent
    skill = _read_skill(here.parent / "SKILL.md")
    variables = context["vars"]
    displayed = variables["displayed"]
    note = variables["note"]
    line = variables.get("line")
    line_block = f"Recipe ingredient line:\n{line}\n\n" if line else ""
    return (
        f"{skill}\n\n"
        "Apply the Writing the resolved link rule.\n\n"
        f"{line_block}"
        f"Displayed word: {displayed}\n"
        f"Resolved note name: {note}\n\n"
        "Output contract: respond with ONLY the wikilink markdown to write, "
        "for example [[leek]]s. Output nothing else."
    )
