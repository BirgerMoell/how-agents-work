# Övning: bygg en agent i åtta steg

Varje fil lägger till en idé till den förra. Läs den, kör den, ändra den. Filerna är 20 till 60 rader
och delar på [`common.py`](common.py): en klient mot modellen, en hjälpfunktion för att beskriva
verktyg, loopen och en färgad utskrift av vad agenten gör. Koden och kommentarerna är på engelska.

## Förberedelser

```bash
ollama pull qwen3.6:35b-a3b      # vilken lokal modell som helst med verktygsstöd fungerar
pip install openai               # klienten; Ollama talar samma API
```

Byt modell med `MODEL=gemma4:e2b python 03_agent_loop.py`. Sätt `OPENAI_API_KEY` (och gärna `MODEL`)
för att använda OpenAI i stället för en lokal modell.

## Stegen

| Fil | Idé | Prova |
|---|---|---|
| [`01_chat.py`](01_chat.py) | En chattbot är en lista. Hela listan skickas i varje anrop. | Berätta vad du heter och fråga sedan om det. Se antalet meddelanden växa. |
| [`02_one_tool.py`](02_one_tool.py) | Ett verktyg. Modellen ber, programmet kör funktionen. | ”Vilken veckodag är det i morgon?” |
| [`03_agent_loop.py`](03_agent_loop.py) | Loopen: fortsätt så länge modellen ber om verktyg. Tre verktyg, med godkännande av terminalkommandon. | Kör utan argument, eller `python 03_agent_loop.py "hur många rader Python finns här?"` |
| [`04_context.py`](04_context.py) | En tokenbudget och komprimering genom sammanfattning. Budgeten är liten så att du ser det hända. | Be om långa svar och fråga sedan om något du sa först. |
| [`05_memory.py`](05_memory.py) | Minne i en fil som läses in i systemprompten igen. | Kör den två gånger. |
| [`06_skills.py`](06_skills.py) | Färdigheter: bara beskrivningar i kontexten, fullständiga instruktioner vid behov. | ”Skriv en haiku om regn.” Lägg sedan till en mapp under `skills/`. |
| [`07_subagent.py`](07_subagent.py) | Underagenter: en ny kontextlista som körs genom samma loop. | Kör utan indata. Se hur lite som kommer tillbaka till huvudagenten. |
| [`08_heartbeat.py`](08_heartbeat.py) | Självständighet: vakna på en timer, följ `HEARTBEAT.md`, logga resultatet. | Lägg en fil som heter `inbox.txt` bredvid. Avsluta med Ctrl+C. |

Modellerna förstår svenska, så du kan skriva till agenterna på svenska.

## Säkerhet

Steg 3 har ett `bash`-verktyg. Det frågar före varje kommando, och allt annat svar än `y` avböjer.
Behåll det så om du inte kör agenten i en container eller på en dator du kan slänga. Steg 5 och 8
skriver `memory.md`, `HEARTBEAT.md` och `heartbeat-log.md` i den aktuella mappen.
