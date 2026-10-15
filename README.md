# How AI agents work

**An agent is a language model in a loop that can use tools.** This repository explains that
sentence from the ground up, in English and Swedish, four ways:

| | English | Svenska |
|---|---|---|
| Interactive guide | [birgermoell.github.io/how-agents-work](https://birgermoell.github.io/how-agents-work/) | [/sv/](https://birgermoell.github.io/how-agents-work/sv/) |
| Video (7–9 min) | [how-agents-work.en.mp4](docs/video/how-agents-work.en.mp4) | [how-agents-work.sv.mp4](docs/video/how-agents-work.sv.mp4) |
| Animated presentation | [present](https://birgermoell.github.io/how-agents-work/explainer/?lang=en&mode=present) | [presentera](https://birgermoell.github.io/how-agents-work/explainer/?lang=sv&mode=present) |
| Runnable code | [`practice/`](practice/) | [`practice/README.sv.md`](practice/README.sv.md) |

[Svensk README](README.sv.md)

## What you will learn

1. **The model** predicts the next token. It has no memory, no clock and no hands.
2. **A chat is a list.** The program keeps the messages and sends the whole list every call. That list is the context.
3. **Tools.** The model asks for a function to be called; the program runs it and adds the result.
4. **The loop.** Keep calling the model while it asks for tools. That is the agent.
5. **A real run**, recorded on a laptop with a local model.
6. **The shell** as one tool that unlocks thousands of abilities, and why that is dangerous.
7. **Context engineering**: what fills the context, why it costs, and how compaction works.
8. **Memory** across sessions, with search and forgetting.
9. **Skills**: know-how that is loaded only when needed.
10. **Sub-agents**: another context list, run through the same loop.
11. **Autonomy**: a heartbeat that wakes the agent with a checklist.
12. **Safety**: prompt injection, least access, human approval, logging.

## Run the code

```bash
# 1. a local model with tool support (no API key needed)
ollama pull qwen3.6:35b-a3b          # or: export MODEL=gemma4:e2b on a smaller machine

# 2. the steps
git clone https://github.com/BirgerMoell/how-agents-work
cd how-agents-work/practice
pip install openai
python 01_chat.py                     # then 02, 03 ... 08
```

To use OpenAI instead, set `OPENAI_API_KEY` and `MODEL`. See [`practice/README.md`](practice/README.md).

## How the video is made

Every frame is drawn by code. The scenes in [`docs/explainer/scenes.js`](docs/explainer/scenes.js)
are pure functions of time, drawn on a canvas by [`engine.js`](docs/explainer/engine.js). The same
code runs three ways:

- in the browser, synced to the narration ([watch mode](https://birgermoell.github.io/how-agents-work/explainer/));
- as a live presentation, where each key press plays the next step ([present mode](https://birgermoell.github.io/how-agents-work/explainer/?mode=present));
- frame by frame in headless Chromium, piped to ffmpeg ([`video/render.py`](video/render.py)).

The narration is written in [`video/script.en.json`](video/script.en.json) and
[`video/script.sv.json`](video/script.sv.json), and synthesised one sentence at a time with local
voices: Kokoro 82M for English (local) and the ElevenLabs voice Elin Nilsson for Swedish ([`video/narrate.py`](video/narrate.py); Supertonic 3 is the local Swedish alternative).
Sentence timings become the cues the animations are synced to. Every narration sentence was checked by
transcribing it back with a local speech recogniser.

```bash
uv run video/narrate.py en            # -> build/en/narration.wav, docs/explainer/timeline.en.json
python video/render.py en             # -> docs/video/how-agents-work.en.mp4 (+ .srt, .vtt)
python video/render.py en --stills 12.5 40   # single frames for checking
```

`render.py` needs `playwright` (then `playwright install chromium`) and `imageio-ffmpeg`.
To change the explainer, edit the scene, render a few stills, then render the video.

## Sources

- [Lecture 9: AI Agents, acting in the world through tools](https://www.youtube.com/watch?v=DS6cwCkN5lg&t=173s), Birger Moëll
- [Lecture 8: Context Engineering](https://www.youtube.com/watch?v=bnNSgrAEQiU&t=699s), Birger Moëll
- [BirgerMoell/agents](https://github.com/BirgerMoell/agents): agents from scratch, with skills, local models and workshop demos
- [You Should Write An Agent](https://fly.io/blog/everyone-write-an-agent/), Thomas Ptacek, Fly.io, 6 November 2025
- [Agent Skills](https://agentskills.io), the open skill format
- [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) and [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), Anthropic
- [Function calling guide](https://platform.openai.com/docs/guides/function-calling), OpenAI
- [OpenClaw](https://github.com/openclaw/openclaw) and [its docs](https://docs.openclaw.ai)
- [The lethal trifecta for AI agents](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/), Simon Willison

## Repository layout

```
docs/                 GitHub Pages site (English at /, Swedish at /sv/)
  explainer/          the animation engine, scenes, timelines, web player and narration audio
  video/              rendered videos, subtitles and posters
practice/             eight runnable steps, from a chat list to a heartbeat
video/                narration scripts and the narrate/render pipeline
```

## Licence

Code: MIT. Text, video and narration: CC BY 4.0. Fonts: Outfit and JetBrains Mono, SIL Open Font Licence.
