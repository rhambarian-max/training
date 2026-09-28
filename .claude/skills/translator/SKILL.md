---
name: translator
description: Translate text or files between Armenian (hy), Russian (ru) and English (en) in any direction, using open-source models that run locally (Meta NLLB-200 by default, Helsinki-NLP OPUS-MT as a fallback). Use when the user asks to translate to or from Armenian, Russian or English, wants an offline or open-source translation, or wants a second opinion on a translation.
---

# Translator: Armenian, Russian, English

Translates in all six directions between **Armenian (hy)**, **Russian (ru)** and **English (en)**
with open-source neural MT models that run locally. No API keys are needed.

## Engines

| Engine | Model | License | Notes |
|---|---|---|---|
| `nllb` (default) | [`facebook/nllb-200-distilled-600M`](https://huggingface.co/facebook/nllb-200-distilled-600M) | CC-BY-NC-4.0 | One model covers all 6 directions. Best Armenian quality of the small open models. **Non-commercial use only.** |
| `nllb-1.3b` | `facebook/nllb-200-distilled-1.3B` | CC-BY-NC-4.0 | Higher quality, needs ~6 GB RAM. |
| `opus` | [Helsinki-NLP OPUS-MT](https://github.com/Helsinki-NLP/Opus-MT) (`opus-mt-{src}-{tgt}`) | CC-BY-4.0 / Apache-2.0 | Commercial-friendly. Small bilingual Marian models. When a direct pair has no model, it pivots through English. |

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

# text argument, source language detected automatically from the script (Armenian/Cyrillic/Latin)
python $S --to en "Բարև, ինչպե՞ս ես։"

# explicit source language
python $S --from ru --to hy "Доброе утро!"

# stdin or file, output to a file
cat letter.txt | python $S --to ru
python $S --to hy --input doc.txt --output doc.hy.txt

# commercial-friendly engine
python $S --engine opus --from en --to hy "Good morning"

# one input into both other languages
python $S --to all "Hello, friend"
```

Options: `--from {hy,ru,en,auto}` (default `auto`), `--to {hy,ru,en,all}`,
`--engine {nllb,nllb-1.3b,opus}`, `--input FILE`, `--output FILE`, `--device {cpu,cuda}`,
`--beams N` (default 4).

The script translates paragraph by paragraph and sentence by sentence, so the layout of
multi-paragraph text is kept and long text does not hit the model's length limit.

## How Claude should use this skill

1. Work out the source and target languages. If the user did not name a target, ask, or pick
   the obvious one (for example Armenian text from an English speaker goes to English).
2. Run `translate.py`. If the dependencies are missing, install them from `requirements.txt`.
   If the model cannot be downloaded (no network to huggingface.co), tell the user, and offer
   to translate directly instead.
3. Review the output yourself before handing it over. Small MT models can garble names,
   numbers, idioms and formal/informal address (Russian ты/вы, Armenian դու/դուք). Fix clear
   errors and say what you changed.
4. For Armenian, the models write **Eastern Armenian** in reformed orthography. Say so if the
   user seems to need Western Armenian or classical orthography, and adapt the text by hand.
5. Give the translation first, then any short notes (ambiguities, terms left as-is).
