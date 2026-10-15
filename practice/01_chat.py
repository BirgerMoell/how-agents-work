"""Step 1: a chatbot is a list.

The language model has no memory. What looks like a conversation is a program that keeps every
message in a list and sends the whole list every time. That list is the context.
"""
from common import YELLOW, ask, call, show

context = [{"role": "system", "content": "You are a helpful assistant. Answer briefly."}]

while True:
    line = ask()
    if not line:
        continue
    context.append({"role": "user", "content": line})
    reply = call(context)
    context.append({"role": "assistant", "content": reply.content})
    show("model", reply.content, YELLOW)
    show("context", f"{len(context)} messages were sent in this call")
