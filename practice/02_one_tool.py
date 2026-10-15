"""Step 2: one tool.

The model cannot know what time it is. We describe a function to it. The model never runs the
function itself: it replies with a request ("call clock"), our program runs the function and puts
the result in the context, and then we ask the model again.
"""
from datetime import datetime

from common import BLUE, GREEN, YELLOW, as_message, ask, call, show, tool

TOOLS = [tool("clock", "Returns the current local date and time.")]


def clock():
    return datetime.now().strftime("%A %d %B %Y, %H:%M")


context = [{"role": "system", "content": "You are a helpful assistant. Answer briefly."},
           {"role": "user", "content": ask("You: ") or "What day of the week is it tomorrow?"}]

reply = call(context, TOOLS)
context.append(as_message(reply))

for request in reply.tool_calls or []:
    show("wants", f"{request.function.name}()", BLUE)
    result = clock()
    show("result", result, GREEN)
    context.append({"role": "tool", "tool_call_id": request.id, "content": result})

if reply.tool_calls:
    reply = call(context, TOOLS)
show("model", reply.content, YELLOW)
