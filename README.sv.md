# Så fungerar AI-agenter

**En agent är en språkmodell i en loop som kan använda verktyg.** Det här repot förklarar den
meningen från grunden, på svenska och engelska, på fyra sätt:

| | Svenska | English |
|---|---|---|
| Interaktiv guide | [birgermoell.github.io/how-agents-work/sv](https://birgermoell.github.io/how-agents-work/sv/) | [/](https://birgermoell.github.io/how-agents-work/) |
| Video (7–8 min) | [how-agents-work.sv.mp4](docs/video/how-agents-work.sv.mp4) | [how-agents-work.en.mp4](docs/video/how-agents-work.en.mp4) |
| Animerad presentation | [presentera](https://birgermoell.github.io/how-agents-work/explainer/?lang=sv&mode=present) | [present](https://birgermoell.github.io/how-agents-work/explainer/?lang=en&mode=present) |
| Körbar kod | [`practice/README.sv.md`](practice/README.sv.md) | [`practice/`](practice/) |

[English README](README.md)

## Det här lär du dig

1. **Modellen** förutsäger nästa token. Den har inget minne, ingen klocka och inga händer.
2. **En chatt är en lista.** Programmet sparar meddelandena och skickar hela listan i varje anrop. Listan är kontexten.
3. **Verktyg.** Modellen ber om att en funktion ska anropas; programmet kör den och lägger till resultatet.
4. **Loopen.** Fortsätt anropa modellen så länge den ber om verktyg. Det är agenten.
5. **En riktig körning**, inspelad på en bärbar dator med en lokal modell.
6. **Terminalen** som ett verktyg som låser upp tusentals förmågor, och varför det är farligt.
7. **Kontexthantering**: vad som fyller kontexten, varför den kostar och hur komprimering fungerar.
8. **Minne** mellan sessioner, med sökning och glömska.
9. **Färdigheter** (skills): kunnande som laddas bara när det behövs.
10. **Underagenter**: en annan kontextlista som körs genom samma loop.
11. **Självständighet**: ett hjärtslag som väcker agenten med en checklista.
12. **Säkerhet**: promptinjektion, minsta åtkomst, mänskligt godkännande, loggning.

## Kör koden

```bash
# 1. en lokal modell med verktygsstöd (ingen API-nyckel behövs)
ollama pull qwen3.6:35b-a3b          # eller: export MODEL=gemma4:e2b på en mindre dator

# 2. stegen
git clone https://github.com/BirgerMoell/how-agents-work
cd how-agents-work/practice
pip install openai
python 01_chat.py                     # sedan 02, 03 ... 08
```

Koden och kommentarerna är på engelska. Guiden till stegen finns på svenska i
[`practice/README.sv.md`](practice/README.sv.md).

## Så görs videon

Varje bildruta ritas av kod. Scenerna i [`docs/explainer/scenes.js`](docs/explainer/scenes.js) är
rena funktioner av tiden och ritas på en canvas av [`engine.js`](docs/explainer/engine.js). Samma kod
körs på tre sätt: i webbläsaren i takt med berättarrösten, som en presentation där varje knapptryckning
spelar nästa steg, och bildruta för bildruta i headless Chromium till ffmpeg
([`video/render.py`](video/render.py)).

Manuset finns i [`video/script.sv.json`](video/script.sv.json). Det läses in mening för mening med
lokala röster, Supertonic 3 för svenska och Kokoro 82M för engelska
([`video/narrate.py`](video/narrate.py)), och varje menings starttid styr animationerna. Varje mening
kontrollerades genom att transkriberas tillbaka med en lokal svensk taligenkännare.

```bash
uv run video/narrate.py sv
python video/render.py sv
```

## Källor

Se [README.md](README.md#sources) eller guiden.

## Licens

Kod: MIT. Text, video och berättarröst: CC BY 4.0. Typsnitt: Outfit och JetBrains Mono, SIL Open Font Licence.
