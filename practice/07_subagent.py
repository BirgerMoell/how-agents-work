"""Step 7: sub-agents.

A sub-agent is not a new kind of thing. It is another context list with its own instructions
and tools, run through the same loop. The main agent gets a tool that starts one. The sub-agent
can read many files, and only its short answer comes back, so the main context stays clean.
"""
import pathlib

from common import YELLOW, ask, loop, show, tool

READ_TOOLS = [tool("list_files", "List the files in a folder.", path="Folder path"),
              tool("read_file", "Read a text file.", path="File path")]


def read_only(name, a):
    if name == "list_files":
        return "\n".join(sorted(p.name for p in pathlib.Path(a["path"]).iterdir()))
    return pathlib.Path(a["path"]).read_text()[:20_000]


def delegate(name, a):
    """Run a fresh agent with an empty context. Return only its final answer."""
    sub_context = [{"role": "system", "content": "You are a research sub-agent. Investigate with your "
                                                 "tools, then report your findings in at most 80 words."},
                   {"role": "user", "content": a["task"]}]
    return loop(sub_context, READ_TOOLS, read_only, label="  sub ")


TOOLS = [tool("delegate", "Give a self-contained research task to a sub-agent that can read files. "
                          "You receive its short report.", task="The task, with all needed details")]

task = ask("You: ") or ("Compare 01_chat.py and 03_agent_loop.py in this folder and explain "
                          "the single most important difference. Use sub-agents to read them.")
context = [{"role": "system", "content": "You are a lead agent. Delegate reading to sub-agents, "
                                         "then answer the user briefly."},
           {"role": "user", "content": task}]
show("model", loop(context, TOOLS, delegate, label="main "), YELLOW)
