"""Step 5: memory that survives a restart.

The context disappears when the program stops. Memory is just a file: the agent gets a tool to
write to it, and the file is read into the system prompt at the start of the next session.
Run this twice. Tell it something about yourself the first time and ask about it the second time.
"""
import datetime
import pathlib

from common import YELLOW, ask, loop, show, tool

MEMORY = pathlib.Path("memory.md")
TOOLS = [tool("remember", "Save one short fact worth remembering in future sessions.", fact="The fact")]


def execute(name, a):
    with MEMORY.open("a") as f:
        f.write(f"- {datetime.date.today()}: {a['fact']}\n")
    return "saved"


remembered = MEMORY.read_text() if MEMORY.exists() else "(nothing yet)"
context = [{"role": "system", "content":
            "You are a personal assistant. Save facts about the user that will matter later, "
            "and nothing else.\n\nWhat you remember from earlier sessions:\n" + remembered}]

while True:
    line = ask()
    if line:
        context.append({"role": "user", "content": line})
        show("model", loop(context, TOOLS, execute), YELLOW)
