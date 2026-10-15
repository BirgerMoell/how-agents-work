"""Step 6: skills, knowledge loaded only when needed.

A skill is a folder with a SKILL.md file: a name, a one-line description, then instructions.
Only the names and descriptions go into the context at the start. When a task matches, the agent
calls load_skill and the full instructions enter the context. A hundred skills cost a hundred lines,
not a hundred manuals. The format is the open Agent Skills standard: https://agentskills.io
"""
import pathlib

from common import YELLOW, ask, loop, show, tool

SKILLS = pathlib.Path(__file__).parent / "skills"


def describe(folder):
    """Read name and description from the front matter between the --- lines."""
    head = (folder / "SKILL.md").read_text().split("---")[1]
    meta = dict(line.split(":", 1) for line in head.strip().splitlines())
    return f"- {meta['name'].strip()}: {meta['description'].strip()}"


catalogue = "\n".join(describe(f) for f in sorted(SKILLS.iterdir()) if (f / "SKILL.md").exists())
TOOLS = [tool("load_skill", "Load the full instructions of a skill.", name="Skill name")]


def execute(name, a):
    return (SKILLS / a["name"] / "SKILL.md").read_text()


context = [{"role": "system", "content":
            "You are a helpful agent. When a task matches one of these skills, load it first "
            "and follow it.\n\nAvailable skills:\n" + catalogue}]
show("in context", catalogue)

while True:
    line = ask()
    if line:
        context.append({"role": "user", "content": line})
        show("model", loop(context, TOOLS, execute), YELLOW)
