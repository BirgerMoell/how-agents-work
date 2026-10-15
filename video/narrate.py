#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11,<3.13"
# dependencies = ["mlx-audio", "misaki[en]", "supertonic==1.3.1", "soundfile", "numpy", "huggingface_hub[hf_xet]"]
# ///
"""Synthesise the narration one sentence at a time, so every sentence has an exact start time.

    uv run video/narrate.py en      # Kokoro 82M, voice af_heart
    uv run video/narrate.py sv      # Supertonic 3, voice F1

Writes build/<lang>/narration.wav and docs/explainer/timeline.<lang>.json. The timeline holds
each scene's start, duration and the start of every sentence (the "cues" the animation syncs to).
Both voices run locally, the same models as in https://github.com/BirgerMoell/agents.
"""
import json
import pathlib
import sys

import numpy as np
import soundfile as sf

ROOT = pathlib.Path(__file__).resolve().parent.parent
SR = 24000
LEAD, GAP, TAIL = 0.8, 0.45, 1.1          # seconds of silence: before a scene, between sentences, after
END_HOLD = 2.5                            # extra seconds on the last frame


def voice(lang):
    if lang == "sv":
        from supertonic import TTS
        m = TTS(auto_download=True)
        style = m.get_voice_style(voice_name="F1")

        def say(text):
            a, _ = m.synthesize(text, voice_style=style, lang="sv")
            return resample(np.asarray(a, dtype=np.float32).squeeze(), int(m.sample_rate))
        return say
    from mlx_audio.tts.utils import load_model
    m = load_model("mlx-community/Kokoro-82M-bf16")

    def say(text):
        parts = list(m.generate(text=text, voice="af_heart", speed=1.0, lang_code="a"))
        return resample(np.concatenate([np.asarray(p.audio, dtype=np.float32) for p in parts]), 24000)
    return say


def resample(a, sr):
    if sr == SR:
        return a
    x = np.linspace(0, len(a) - 1, int(len(a) * SR / sr))
    return np.interp(x, np.arange(len(a)), a).astype(np.float32)


def trim(a):
    """Cut leading and trailing silence, judged on a 10 ms loudness envelope, keeping soft onsets."""
    win = SR // 100
    env = np.sqrt(np.convolve(a * a, np.ones(win) / win, mode="same"))
    idx = np.where(env > 0.03 * env.max())[0]
    if not len(idx):
        return a
    return a[max(idx[0] - int(0.12 * SR), 0): idx[-1] + int(0.15 * SR)]


def main(lang):
    script = json.loads((ROOT / f"video/script.{lang}.json").read_text())
    say = voice(lang)
    out = ROOT / "build" / lang
    out.mkdir(parents=True, exist_ok=True)
    audio, scenes, t = [], [], 0.0
    for sc in script["scenes"]:
        start, cues, lines = t, [], []
        audio.append(np.zeros(int(LEAD * SR), np.float32))
        t += LEAD
        for i, line in enumerate(sc["lines"]):
            a = trim(say(line)) * 0.9
            sf.write(out / f"{sc['id']}_{i:02d}.wav", a, SR)
            cues.append(round(t - start, 3))
            lines.append({"text": line, "start": round(t, 3), "end": round(t + len(a) / SR, 3)})
            audio += [a, np.zeros(int(GAP * SR), np.float32)]
            t += len(a) / SR + GAP
            print(f"{sc['id']:>10} {i} {len(a) / SR:5.1f}s  {line[:70]}", flush=True)
        audio.append(np.zeros(int((TAIL - GAP) * SR), np.float32))
        t += TAIL - GAP
        scenes.append({"id": sc["id"], "chapter": sc["chapter"], "start": round(start, 3),
                       "dur": round(t - start, 3), "cues": cues, "lines": lines})
    audio.append(np.zeros(int(END_HOLD * SR), np.float32))
    t += END_HOLD
    scenes[-1]["dur"] = round(scenes[-1]["dur"] + END_HOLD, 3)
    sf.write(out / "narration.wav", np.concatenate(audio), SR)
    tl = {"lang": lang, "title": script["title"], "duration": round(t, 3), "end_hold": END_HOLD, "scenes": scenes}
    (ROOT / f"docs/explainer/timeline.{lang}.json").write_text(json.dumps(tl, ensure_ascii=False, indent=1))
    print(f"total {t / 60:.1f} min")


if __name__ == "__main__":
    main(sys.argv[1])
