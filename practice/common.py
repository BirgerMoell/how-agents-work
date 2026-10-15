"""Shared by every step: a client for the language model and a printout of what the agent does.

The default is a local model in Ollama, so no API key is needed. Environment variables switch it:

    MODEL=gemma4:e2b python 03_agent_loop.py              # another local model
    OPENAI_API_KEY=sk-... MODEL=gpt-5.2 python ...        # OpenAI instead of Ollama
"""
import json
import os

from openai import OpenAI

if os.getenv("OPENAI_API_KEY"):
    client = OpenAI()
    MODEL = os.getenv("MODEL", "gpt-5.2")
else:
    client = OpenAI(base_url=os.getenv("OLLAMA_URL", "http://127.0.0.1:11434/v1"), api_key="ollama")
    MODEL = os.getenv("MODEL", "qwen3.6:35b-a3b")

GREY, YELLOW, BLUE, GREEN, RED, RESET = "\033[90m", "\033[33m", "\033[36m", "\033[32m", "\033[31m", "\033[0m"


def call(context, tools=None):
    """One call to the model. The whole context is sent every time: the model remembers nothing."""
    response = client.chat.completions.create(model=MODEL, messages=context, tools=tools or None)
    return response.choices[0].message


def tool(name, description, /, **params):
    """Describe a tool in the format models are trained on (JSON Schema). Every parameter is a string."""
    return {"type": "function", "function": {
        "name": name, "description": description,
        "parameters": {"type": "object",
                       "properties": {p: {"type": "string", "description": d} for p, d in params.items()},
                       "required": list(params)}}}


def as_message(msg):
    """Turn the model's reply back into a plain message that can go into the context again."""
    m = {"role": "assistant", "content": msg.content or ""}
    if msg.tool_calls:
        m["tool_calls"] = [{"id": c.id, "type": "function",
                            "function": {"name": c.function.name, "arguments": c.function.arguments}}
                           for c in msg.tool_calls]
    return m


def args(tool_call):
    try:
        return json.loads(tool_call.function.arguments or "{}")
    except json.JSONDecodeError:
        return {}


def loop(context, tools, execute, max_steps=12, label=""):
    """The loop from step 3, packaged so the later steps can reuse it.

    execute(name, args) runs one tool and returns a string. The loop ends when the model answers
    without asking for a tool.
    """
    for step in range(1, max_steps + 1):
        reply = call(context, tools)
        context.append(as_message(reply))
        if not reply.tool_calls:
            return reply.content
        for request in reply.tool_calls:
            a = args(request)
            show(f"{label}step {step}", f"{request.function.name}({a})", BLUE)
            try:
                result = execute(request.function.name, a)
            except Exception as e:
                result = f"error: {e}"
            show("result", result, GREEN)
            context.append({"role": "tool", "tool_call_id": request.id, "content": str(result)})
    return "Stopped: too many steps."


def ask(prompt="\nYou: "):
    """Read a line from the user; end the program cleanly on Ctrl+D or Ctrl+C."""
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        raise SystemExit(0)


def show(role, text, colour=GREY):
    text = " ".join(str(text).split())
    if len(text) > 300:
        text = text[:300] + f" … ({len(text)} chars)"
    print(f"{colour}{role:>10}{RESET}  {text}")
