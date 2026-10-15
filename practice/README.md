# Practice: build an agent in eight steps

Each file adds one idea to the one before. Read it, run it, change it. They are 20 to 60 lines each,
and they all share [`common.py`](common.py): a client for the model, a helper to describe tools, the
loop, and a coloured printout of what the agent does.

## Setup

```bash
ollama pull qwen3.6:35b-a3b      # any local model with tool support works
pip install openai               # the client; Ollama speaks the same API
```

Change model with `MODEL=gemma4:e2b python 03_agent_loop.py`. To use OpenAI instead of a local model,
set `OPENAI_API_KEY` (and optionally `MODEL`).

## The steps

| File | Idea | What to try |
|---|---|---|
| [`01_chat.py`](01_chat.py) | A chatbot is a list. The whole list is sent every call. | Tell it your name, then ask for it. Watch the message count grow. |
| [`02_one_tool.py`](02_one_tool.py) | One tool. The model asks, the program runs the function. | "What day of the week is it tomorrow?" |
| [`03_agent_loop.py`](03_agent_loop.py) | The loop: keep going while the model asks for tools. Three tools, with approval for shell commands. | Run with no arguments, or `python 03_agent_loop.py "how many lines of Python are here?"` |
| [`04_context.py`](04_context.py) | A token budget and compaction by summary. The budget is tiny so you see it happen. | Ask for long answers, then ask about something you said first. |
| [`05_memory.py`](05_memory.py) | Memory in a file, read back into the system prompt. | Run it twice. |
| [`06_skills.py`](06_skills.py) | Skills: only descriptions in context, full instructions on demand. | "Write a haiku about rain." Then add a folder under `skills/`. |
| [`07_subagent.py`](07_subagent.py) | Sub-agents: a fresh context list run through the same loop. | Run with no input. Note how little comes back to the main agent. |
| [`08_heartbeat.py`](08_heartbeat.py) | Autonomy: wake on a timer, follow `HEARTBEAT.md`, log the result. | Put a file called `inbox.txt` next to it. Stop with Ctrl+C. |

Every step was run against `qwen3.6:35b-a3b` in Ollama on a laptop. Steps 3 and 7 also run on
the much smaller `gemma4:e2b`.

## Safety

Step 3 has a `bash` tool. It asks before every command, and answering anything but `y` refuses.
Keep it that way unless you run the agent in a container or a throwaway machine. Steps 5 and 8 write
`memory.md`, `HEARTBEAT.md` and `heartbeat-log.md` in the current folder.
