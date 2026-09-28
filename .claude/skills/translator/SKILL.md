---
name: translator
description: Translate Armenian (hy) text or files into Russian, English, or both at once, using open-source models that run locally (Meta NLLB-200 by default, Helsinki-NLP OPUS-MT as a commercial-friendly fallback). Use when the user gives Armenian text and wants it in Russian and/or English, or asks for an offline or open-source Armenian translation. Not for translating into Armenian or between Russian and English.
---

# Translator: Armenian → Russian / English

Translates **Armenian (hy)** into **Russian (ru)**, **English (en)**, or both at once, with
open-source neural MT models that run locally. No API keys are needed.

Armenian is the only source language. The script refuses input that is not mostly Armenian.

## Engines

| Engine | Model | License | Notes |
|---|---|---|---|
| `nllb` (default) | [`facebook/nllb-200-distilled-600M`](https://huggingface.co/facebook/nllb-200-distilled-600M) | CC-BY-NC-4.0 | One model covers hy→ru and hy→en. Best Armenian quality of the small open models. **Non-commercial use only.** |
| `nllb-1.3b` | `facebook/nllb-200-distilled-1.3B` | CC-BY-NC-4.0 | Higher quality, needs ~6 GB RAM. |
| `opus` | [Helsinki-NLP OPUS-MT](https://github.com/Helsinki-NLP/Opus-MT): `opus-mt-hy-ru`, `opus-mt-hy-en` | CC-BY-4.0 / Apache-2.0 | Commercial-friendly small Marian models. If `opus-mt-hy-en` is unavailable, hy→en goes through Russian (hy→ru→en). |

Argos Translate / LibreTranslate were considered but have no Armenian package, so they are not used.

## Setup (once)

```bash
pip install -r .claude/skills/translator/scripts/requirements.txt
```

The first run downloads the model from Hugging Face (about 2.5 GB for NLLB-600M) into the
Hugging Face cache. After that it works offline.

## Usage

```bash
S=.claude/skills/translator/scripts/translate.py

# into both Russian and English (default)
python $S "Բարև, ինչպե՞ս ես։"

# into one language only
python $S --to ru "Բարի լույս։"
python $S --to en "Բարի լույս։"

# stdin or file, output to a file
cat letter.hy.txt | python $S
python $S --to ru --input doc.hy.txt --output doc.ru.txt

# commercial-friendly engine
python $S --engine opus "Շնորհակալություն"
```

Options: `--to {ru,en,all}` (default `all`), `--engine {nllb,nllb-1.3b,opus}`,
`--input FILE`, `--output FILE`, `--device {cpu,cuda}`, `--beams N` (default 4).

With `--to all`, the output has a `[Russian]` block and then an `[English]` block.
The script translates paragraph by paragraph and sentence by sentence (splitting on `։` and `.`),
so the layout of multi-paragraph text is kept and long text does not hit the model's length limit.

## How Claude should use this skill

1. Confirm the text is Armenian. If the user did not say which target they want, translate into
   both Russian and English.
2. Run `translate.py`. If the dependencies are missing, install them from `requirements.txt`.
   If the model cannot be downloaded (no network to huggingface.co), tell the user, and offer
   to translate directly instead.
3. Review the output yourself before handing it over. Small MT models can garble names,
   numbers, dates, idioms, and formal/informal address (Armenian դու/դուք should become
   Russian ты/вы and be consistent throughout). Fix clear errors and say what you changed.
4. Names: transliterate Armenian names the standard way for each language (for example
   Գևորգ → Геворг / Gevorg), and keep them the same everywhere in the text.
5. The models are trained mostly on **Eastern Armenian**. If the source is Western Armenian
   or classical orthography, warn that quality may drop and check the result more carefully.
6. Give the Russian translation first, then the English one, then any short notes
   (ambiguities, terms left as-is).
