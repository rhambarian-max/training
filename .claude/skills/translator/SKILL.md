---
name: translator
description: Translate Armenian (hy) banking and financial texts and files (loan and deposit agreements, account statements, tariffs, Central Bank regulations, AML/KYC documents, bank correspondence, .txt or .docx) into Russian, English, or both, using open-source models that run locally so client data stays on the machine. Uses a banking glossary and checks that every amount, rate, date and account number is carried over. Use when the user gives Armenian banking or financial text and wants it in Russian and/or English. Not for translating into Armenian or between Russian and English.
---

# Banking translator: Armenian → Russian / English

Translates **Armenian (hy)** banking and financial texts into **Russian (ru)**, **English (en)**,
or both at once. Typical inputs: loan, deposit and guarantee agreements, account statements,
tariffs and fee schedules, Central Bank of Armenia (CBA) regulations and letters, AML/KYC
questionnaires, client letters and complaints, financial statements.

Armenian is the only source language. The script refuses input that is not mostly Armenian.

## Confidentiality

Banking texts contain client names, account numbers, amounts and other data covered by
**banking secrecy** (ՀՀ «Բանկային գաղտնիքի մասին» օրենք). That is why translation runs on
local open-source models: the text never leaves the machine.

- Never send the text, or pieces of it, to online translators, web search or any other external service.
- Do not copy client data into commit messages, issues, published pages or other shared places.
- Keep translated files next to the originals (or where the user says), not in public folders.

## Engines

| Engine | Model | License | Notes |
|---|---|---|---|
| `nllb-1.3b` (default) | `facebook/nllb-200-distilled-1.3B` | CC-BY-NC-4.0 | Best quality of the small open models; the default because accuracy matters in banking. ~5.5 GB download, ~8 GB RAM. |
| `nllb-600m` | [`facebook/nllb-200-distilled-600M`](https://huggingface.co/facebook/nllb-200-distilled-600M) | CC-BY-NC-4.0 | Faster, for weaker machines (~2.5 GB, ~4 GB RAM). Lower quality. |
| `opus` | [Helsinki-NLP OPUS-MT](https://github.com/Helsinki-NLP/Opus-MT): `opus-mt-hy-ru`, `opus-mt-hy-en` | CC-BY-4.0 / Apache-2.0 | Allowed for commercial use. If `opus-mt-hy-en` is unavailable, hy→en goes through Russian. |

**License:** NLLB is licensed for non-commercial use only. For translating a bank's working
documents as part of its business, use `--engine opus`, or have the bank's legal team confirm NLLB is acceptable.

## Setup (once)

```bash
pip install -r .claude/skills/translator/scripts/requirements.txt
```

The first run downloads the model from Hugging Face into the Hugging Face cache. After that it works offline.

## Usage

```bash
S=.claude/skills/translator/scripts/translate.py

# into both Russian and English (default)
python $S "Վարկի տարեկան տոկոսադրույքը 12,5% է։"

# one language only
python $S --to ru "Ավանդի մնացորդը 250 000 ՀՀ դրամ է։"

# plain text file
python $S --to en --input letter.txt --output letter.en.txt

# Word file: writes agreement.ru.docx and agreement.en.docx next to the original
python $S --input agreement.docx

# commercial-use engine
python $S --engine opus --input tariffs.docx --to ru
```

Options: `--to {ru,en,all}` (default `all`), `--engine {nllb-1.3b,nllb-600m,opus}`,
`--input FILE` (.txt or .docx), `--output FILE_OR_DIR`, `--device {cpu,cuda}`, `--beams N` (default 4).

For **.docx**, the script translates the body, tables (including nested ones), headers and footers,
and keeps the document structure. Each paragraph takes the formatting of its first run, so bold or
italic words inside a paragraph are lost. For **PDF** or **Excel**, extract the text first (with the
pdf or xlsx skill), translate it, then rebuild the document if needed.

### Automatic checks

After translating, the script compares each paragraph with the source and prints `[review]` lines on stderr:

- **Numbers:** every amount, rate, date and account number in the source must appear in the
  translation. Separators are ignored, so `1 500 000,50` and `1,500,000.50` count as the same number.
- **Terminology:** if a term from `glossary.tsv` is in the source, the expected Russian/English
  term must be in the translation.

The checks can raise false alarms (for example a date rewritten as "15 March 2026"). Check every warning by hand.

## Glossary

`glossary.tsv` (next to this file) lists about 75 banking terms: Armenian, Russian and English,
tab-separated, with the preferred term first and accepted variants after `;`. Use it as the
reference for terminology when reviewing. When the user or the bank has its own preferred terms,
add or change rows there. Keep the Armenian column's inflected forms (e.g. `մարում; մարման`),
since the check matches Armenian words exactly.

## How Claude should use this skill

1. Confirm the text is Armenian. If the user did not say which language they want, translate into
   both Russian and English.
2. Run `translate.py`. If dependencies are missing, install them from `requirements.txt`. If the
   model cannot be downloaded (no network to huggingface.co), tell the user, and offer to translate
   the text yourself in this session instead, following the rules below.
3. **Review the whole translation against the source**, starting with every `[review]` warning.
   Fix errors and tell the user what you changed. Machine translation of banking text needs this step every time.
4. Apply these banking rules in the review:
   - **Figures:** amounts, rates, dates, terms (months/days), account numbers, IBAN, SWIFT/BIC, TIN
     and contract numbers must match the source exactly. Never round or convert.
   - **Number format:** Russian `1 500 000,50`; English `1,500,000.50`. Percentages: `12,5%` / `12.5%`.
   - **Currency:** `ՀՀ դրամ` / `֏` → Russian `драм РА` (or `AMD`) → English `AMD` before the amount
     (`AMD 1,500,000`). Keep USD, EUR, RUB as ISO codes.
   - **Dates:** Russian `15.03.2026` or `15 марта 2026 г.`; English `15 March 2026`. Never write
     `03/15/2026`, which is ambiguous.
   - **Terminology:** use `glossary.tsv`. Use one term per concept throughout a document (don't
     switch between "loan" and "credit" for վարկ).
   - **Legal wording:** in agreements, "պարտավոր է" → "обязан" → "shall"; "իրավունք ունի" →
     "вправе" / "имеет право" → "may" / "is entitled to". Do not soften or strengthen obligations.
   - **Laws and institutions:** use their official names, e.g. ՀՀ «Բանկերի և բանկային գործունեության
     մասին» օրենք → Закон РА «О банках и банковской деятельности» → Law of the RA "On Banks and
     Banking Activity"; ՀՀ կենտրոնական բանկ → Центральный банк РА → Central Bank of Armenia (CBA).
   - **Bank names:** use the bank's own official Russian/English name (e.g. from its website) rather than translating it.
   - **Personal names:** transliterate consistently (Գևորգ → Геворг / Gevorg), matching the
     passport spelling if the document gives one.
   - **Address:** client letters use the formal "you": Armenian դուք/Դուք → Russian Вы.
5. The models are trained mostly on **Eastern Armenian**. Warn if the source is Western Armenian
   or classical orthography, and review more carefully.
6. Deliver the Russian translation first, then the English one, then short notes: changes you made
   to the machine output, ambiguous terms, and anything left untranslated.
7. Machine translation is **not a certified translation**. Say so when a document looks legally
   binding or is meant for a court, regulator or notary, since those need a sworn translator.
