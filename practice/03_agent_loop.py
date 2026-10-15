"""Step 3: the loop. This is the whole agent.

Step 2 asked the model once, ran a tool, and asked again. An agent keeps going: as long as the
model asks for tools, we run them and ask again. When it answers without a tool call, it is done.
The model decides how many steps it needs. We only set an upper limit.
"""
import pathlib
import subprocess
import sys

from common import BLUE, GREEN, RED, RESET, YELLOW, args, as_message, call, show, tool

TOOLS = [
    tool("list_files", "List the files in a folder.", path="Folder path, for example ."),
    tool("read_file", "Read a text file.", path="File path"),
    tool("bash", "Run a shell command and return its output. Use with care.", command="The command"),
]


def run(name, a):
    if name == "list_files":
        return "\n".join(sorted(p.name for p in pathlib.Path(a.get("path", ".")).iterdir()))
    if name == "read_file":
        return pathlib.Path(a["path"]).read_text()[:20_000]
    if name == "bash":
        if input(f"{RED}    allow?{RESET} $ {a['command']}  [y/N] ").lower() != "y":
            return "The user refused to run this command."
        p = subprocess.run(a["command"], shell=True, capture_output=True, text=True, timeout=60)
        return (p.stdout + p.stderr)[-20_000:] or "(no output)"
    return f"error: unknown tool {name}"


MAX_STEPS = 12


def agent(task):
    context = [{"role": "system", "content": "You are a careful agent. Use tools to find out, never guess. "
                                             "When you are done, answer briefly."},
               {"role": "user", "content": task}]
    for step in range(1, MAX_STEPS + 1):
        reply = call(context, TOOLS)
        context.append(as_message(reply))
        if not reply.tool_calls:                       # no tool requested: the agent is done
            return reply.content
        for request in reply.tool_calls:
            a = args(request)
            show(f"step {step}", f"{request.function.name}({a})", BLUE)
            try:
                result = run(request.function.name, a)
            except Exception as e:                     # errors go back to the model, it can recover
                result = f"error: {e}"
            show("result", result, GREEN)
            context.append({"role": "tool", "tool_call_id": request.id, "content": result})
    return "Stopped: too many steps."


if __name__ == "__main__":
    task = " ".join(sys.argv[1:]) or "Which Python file in this folder is the longest, and what does it do?"
    show("task", task)
    show("answer", agent(task), YELLOW)
