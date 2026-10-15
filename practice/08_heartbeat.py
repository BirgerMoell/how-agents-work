"""Step 8: autonomy with a heartbeat.

So far the agent only acts when you type. A heartbeat wakes it on a timer. Each beat, it reads a
plain text file (HEARTBEAT.md) that says what to check, does the work, and goes back to sleep.
You stay in control by editing the file. OpenClaw uses the same pattern, by default every 30 min.
"""
import datetime
import pathlib
import time

from common import YELLOW, loop, show, tool

HEARTBEAT = pathlib.Path("HEARTBEAT.md")
LOG = pathlib.Path("heartbeat-log.md")
EVERY_SECONDS = 60

if not HEARTBEAT.exists():
    HEARTBEAT.write_text("- If there is a file called inbox.txt, summarise it in one sentence.\n"
                         "- If nothing needs attention, answer exactly: NOTHING TO DO\n")

TOOLS = [tool("list_files", "List the files in a folder.", path="Folder path"),
         tool("read_file", "Read a text file.", path="File path")]


def execute(name, a):
    if name == "list_files":
        return "\n".join(sorted(p.name for p in pathlib.Path(a["path"]).iterdir()))
    return pathlib.Path(a["path"]).read_text()[:20_000]


while True:
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    context = [{"role": "system", "content": f"You are an autonomous assistant. It is {now}. "
                                             "Follow the checklist. Be brief."},
               {"role": "user", "content": HEARTBEAT.read_text()}]
    result = loop(context, TOOLS, execute, label="beat ")
    show(now, result, YELLOW)
    if "NOTHING TO DO" not in result:
        with LOG.open("a") as f:
            f.write(f"## {now}\n{result}\n\n")
    time.sleep(EVERY_SECONDS)
