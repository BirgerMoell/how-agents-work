// Interactive trace stepper: replays a real recorded agent run one event at a time and shows
// what the context list looks like after each step, and how many tokens each call re-sends.
(async () => {
  const root = document.querySelector("[data-sim]");
  if (!root) return;
  const sv = document.documentElement.lang === "sv";
  const T = sv
    ? { next: "Nästa steg ▶", reset: "Börja om", size: "kontextens storlek", sent: "skickat totalt hittills", step: "steg", done: "Klart: modellen svarade utan verktygsanrop.",
        system: "system", user: "användare", call: "verktygsanrop", result: "verktygsresultat", assistant: "svar", allow: "godkännande" }
    : { next: "Next step ▶", reset: "Reset", size: "context size", sent: "sent in total so far", step: "step", done: "Done: the model answered without a tool call.",
        system: "system", user: "user", call: "tool call", result: "tool result", assistant: "answer", allow: "approval" };
  const trace = await (await fetch(root.dataset.sim)).json();
  const SYSTEM = "You are a careful agent. Use tools to find out, never guess. When you are done, answer briefly.\n[+ descriptions of 3 tools: list_files, read_file, bash]";
  // group the flat event list into rounds: one model call each
  const rounds = [];
  let cur = null;
  for (const e of trace.events) {
    if (e.role === "task") rounds.push({ add: [["user", e.text]] });
    else if (e.role.startsWith("step")) { cur = { add: [["call", e.text]] }; rounds.push(cur); }
    else if (e.role === "allow?") cur.add.push(["allow", "$ " + e.text + "   → y"]);
    else if (e.role === "result") cur.add.push(["result", e.text]);
    else if (e.role === "answer") rounds.push({ add: [["assistant", e.text]] });
  }
  const tok = (s) => Math.ceil(s.length / 4);
  const box = root.querySelector(".msgs"), meter = root.querySelector(".meter");
  let i = 0, ctx = [], sent = 0;
  const render = (m) => {
    const d = document.createElement("div");
    d.className = "msg " + m[0];
    d.innerHTML = `<div class="r"><span>${T[m[0]]}</span><span>~${tok(m[1])} tok</span></div><div class="b"></div>`;
    d.querySelector(".b").textContent = m[1].replace(/\*\*/g, "");
    box.appendChild(d);
    box.scrollTop = box.scrollHeight;
  };
  const update = () => {
    const size = ctx.reduce((a, m) => a + tok(m[1]), 0);
    meter.innerHTML = `${T.size}: <b>~${size} tokens</b> · ${T.sent}: <b>~${sent} tokens</b>
      <div class="bar"><i style="width:${Math.min(100, size / 30)}%"></i></div>`;
  };
  const reset = () => { i = 0; box.innerHTML = ""; ctx = [["system", SYSTEM]]; sent = 0; render(ctx[0]); update(); };
  const next = () => {
    if (i >= rounds.length) return;
    const r = rounds[i++];
    // every model call re-sends the whole context so far
    if (r.add[0][0] !== "user") sent += ctx.reduce((a, m) => a + tok(m[1]), 0);
    r.add.forEach((m) => { ctx.push(m); render(m); });
    if (i === rounds.length) { const d = document.createElement("p"); d.className = "note"; d.textContent = T.done; box.appendChild(d); }
    update();
  };
  root.querySelector("[data-next]").textContent = T.next;
  root.querySelector("[data-reset]").textContent = T.reset;
  root.querySelector("[data-next]").onclick = next;
  root.querySelector("[data-reset]").onclick = reset;
  reset();
})();

// light/dark toggle, remembered per browser
(() => {
  const b = document.querySelector("[data-theme-toggle]");
  if (!b) return;
  try { const t = localStorage.getItem("theme"); if (t) document.documentElement.dataset.theme = t; } catch {}
  b.onclick = () => {
    const dark = getComputedStyle(document.documentElement).getPropertyValue("--bg").trim().toLowerCase() === "#08131d";
    const t = dark ? "light" : "dark";
    document.documentElement.dataset.theme = t;
    try { localStorage.setItem("theme", t); } catch {}
  };
})();
