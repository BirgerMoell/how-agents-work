"""Step 4: the context fills up. Compaction.

Every message, tool description and tool result stays in the context and is sent on every call.
Long sessions grow until they no longer fit (and get slow and expensive long before that).

The common fix is compaction: when the context passes a budget, ask the model to summarise the
older part, and replace it with the summary. Keep the system prompt and the most recent messages.
Something is always lost. Deciding what to keep is the engineering problem.
"""
from common import GREY, YELLOW, ask, call, show

BUDGET = 1_500          # tokens; tiny on purpose so you see compaction happen. Real agents: ~100k+
KEEP_RECENT = 4         # the newest messages are kept word for word


def tokens(context):
    """Rough count: about four characters per token for English text."""
    return sum(len(str(m.get("content") or "")) for m in context) // 4


def compact(context):
    system, old, recent = context[0], context[1:-KEEP_RECENT], context[-KEEP_RECENT:]
    transcript = "\n".join(f"{m['role']}: {m['content']}" for m in old)
    summary = call([{"role": "user", "content":
                     "Summarise this conversation in under 120 words. Keep names, numbers, decisions "
                     "and open questions. Drop small talk.\n\n" + transcript}]).content
    show("compact", f"{len(old)} messages ({tokens(old)} tokens) -> summary ({len(summary) // 4} tokens)", GREY)
    return [system, {"role": "user", "content": f"[Summary of the earlier conversation]\n{summary}"}] + recent


context = [{"role": "system", "content": "You are a helpful assistant."}]
while True:
    line = ask()
    if not line:
        continue
    context.append({"role": "user", "content": line})
    if tokens(context) > BUDGET and len(context) > KEEP_RECENT + 2:
        context = compact(context)
    reply = call(context)
    context.append({"role": "assistant", "content": reply.content})
    show("model", reply.content, YELLOW)
    show("context", f"{len(context)} messages, ~{tokens(context)} of {BUDGET} tokens")
