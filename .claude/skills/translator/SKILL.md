---
name: translator
description: Translate Armenian (hy) banking and financial texts and files (loan and deposit agreements, account statements, tariffs, app and interface texts, Central Bank regulations, AML/KYC documents, client letters, .txt or .docx) into Russian, English, or both, in the style of a Russian- or English-speaking bank. Claude translates by default, following a banking style guide, glossary and reference translations, then checks every amount, rate, date and term with a script; local open-source models (NLLB-200, OPUS-MT) are available when the text must not leave the machine. Use when the user gives Armenian banking or financial text and wants it in Russian and/or English. Not for translating into Armenian or between Russian and English.
---

# Banking translator: Armenian → Russian / English

## Two modes

| Mode | Who translates | When |
|---|---|---|
| **Claude (default)** | Claude, in this session, following `references/style-guide.md`, `glossary.tsv` and `references/examples.md` | Normally. Much better quality than the local models, especially for Armenian. |
| **Local** | Open-source models on this machine (`scripts/translate.py`) | When the user says the text must not leave their machine (e.g. real client data under banking secrecy), or asks for local/offline translation. Claude then reviews the output. |

In both modes the result is checked with `scripts/check.py` (numbers, dates and glossary terms)
and reviewed against the style guide.

Translates **Armenian (hy)** banking and financial texts into **Russian (ru)**, **English (en)**,
or both at once. Typical inputs: loan, deposit and guarantee agreements, account statements,
tariffs and fee schedules, Central Bank of Armenia (CBA) regulations and letters, AML/KYC
questionnaires, client letters and complaints, financial statements.

Armenian is the only source language. The script refuses input that is not mostly Armenian.

## Confidentiality

Banking texts can contain client names, account numbers, amounts and other data covered by
**banking secrecy** (ՀՀ «Բանկային գաղտնիքի մասին» օրենք). In Claude mode the text is processed
by Claude, like anything else shared in this conversation; in local mode it never leaves the machine.

- If the text contains real client data (names, passport data, account numbers, balances) and the
  user has not said Claude mode is acceptable, say so briefly and offer local mode or masking
  (replace names and account numbers with placeholders like [CLIENT], [ACCOUNT] before translating).

- Never send the text, or pieces of it, to online translators, web search or any other external service.
  Terms may be looked up on the web, but never whole sentences with client data.
- Do not copy client data into commit messages, issues, published pages or other shared places.
- Keep translated files next to the originals (or where the user says), not in public folders.

## Local mode: engines

| Engine | Model | License | Notes |
|---|---|---|---|
| `nllb-1.3b` (default) | `facebook/nllb-200-distilled-1.3B` | CC-BY-NC-4.0 | Best quality of the small open models; the default because accuracy matters in banking. ~5.5 GB download, ~8 GB RAM. |
| `nllb-600m` | [`facebook/nllb-200-distilled-600M`](https://huggingface.co/facebook/nllb-200-distilled-600M) | CC-BY-NC-4.0 | Faster, for weaker machines (~2.5 GB, ~4 GB RAM). Lower quality. |
| `opus` | [Helsinki-NLP OPUS-MT](https://github.com/Helsinki-NLP/Opus-MT): `opus-mt-hy-ru`, `opus-mt-hy-en` | CC-BY-4.0 / Apache-2.0 | Allowed for commercial use. If `opus-mt-hy-en` is unavailable, hy→en goes through Russian. |

**License:** NLLB is licensed for non-commercial use only. For translating a bank's working
documents as part of its business, use `--engine opus`, or have the bank's legal team confirm NLLB is acceptable.

## Local mode: setup (once)

```bash
pip install -r .claude/skills/translator/scripts/requirements.txt
```

The first run downloads the model from Hugging Face into the Hugging Face cache. After that it works offline.

## Local mode: usage

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

`translate.py` checks its own output and prints `[review]` lines on stderr. To check any translation
(for example one Claude wrote), save the source and translations to files and run:

```bash
python .claude/skills/translator/scripts/check.py --source src.hy.txt --ru out.ru.txt --en out.en.txt
```

Put temporary files in the scratchpad, not in the repository. Both scripts compare paragraph by paragraph:

- **Numbers:** every amount, rate, date and account number in the source must appear in the
  translation. Separators are ignored, so `1 500 000,50` and `1,500,000.50` count as the same number,
  and dates match across formats (`25.10.2026`, `2026 թ. հոկտեմբերի 25`, `25 октября 2026`, `25 October 2026`).
- **Terminology:** if a term from `glossary.tsv` is in the source, the expected Russian/English
  term must be in the translation.

The checks can raise false alarms (for example a correct synonym missing from the glossary). Check every
warning by hand, and add correct variants to the glossary when a false alarm repeats.

## Glossary

`glossary.tsv` (next to this file) lists about 100 banking terms: Armenian, Russian and English,
tab-separated, with the preferred term first and accepted variants after `;`. Use it as the
reference for terminology when reviewing. When the user or the bank has its own preferred terms,
add or change rows there. Keep the Armenian column's inflected forms (e.g. `մարում; մարման`),
since the check matches Armenian words exactly.

## How Claude should use this skill

1. Confirm the text is Armenian. If the user did not say which language they want, translate into
   both Russian and English.
2. Read `references/style-guide.md` and `references/examples.md`, and look up the source's terms in
   `glossary.tsv`. Decide the text type (contract, interface, client letter, regulatory): it sets the register.
3. Translate:
   - **Claude mode (default):** translate the text yourself. Rebuild each sentence the way a Russian or
     English bank would write it; do not copy the Armenian word order.
   - **Local mode:** run `scripts/translate.py` (install `requirements.txt` first if needed). If the model
     cannot be downloaded, tell the user and ask whether Claude mode is acceptable.
     Treat the output as a rough draft and rewrite it to the style guide.
4. Run `scripts/check.py` on the translation and resolve every `[review]` warning.
5. Check the wording pitfalls (section 5) and do the self-review (section 6) of the style guide, and apply these rules:
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
6. The style guide and the local models assume **Eastern Armenian** in reformed orthography. If the
   source is Western Armenian or classical orthography, say so and review more carefully.
7. Deliver the Russian translation first, then the English one, then short notes: ambiguous
   terms, choices the user may want to change (e.g. a button label), and anything left untranslated.
   Keep notes short.
8. When the user corrects or approves a translation, offer to add it to `references/examples.md`
   and any new terms to `glossary.tsv`, so later translations follow it.
9. These translations (Claude's or the models') are **not certified translations**. Say so when a document looks legally
   binding or is meant for a court, regulator or notary, since those need a sworn translator.
