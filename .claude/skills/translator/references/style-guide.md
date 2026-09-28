# Banking translation style guide (Armenian → Russian / English)

Read this before translating. The aim is text that reads as if a Russian or English-speaking
bank wrote it, not a word-for-word copy of the Armenian.

## 1. Decide the text type first

| Type | Examples | Russian register | English register |
|---|---|---|---|
| **Contract / legal** | loan, deposit, guarantee agreements; terms and conditions; consents | Official-business style (официально-деловой стиль): «Заемщик обязуется…», «Банк вправе…» | Legal English: "The Borrower shall…", "The Bank may…" Capitalise defined terms. |
| **Interface / app** | buttons, pop-ups, confirmation texts, SMS, push notifications | Short and neutral, as in Russian banking apps: «Погасить», «Подтвердить», «Операция выполнена» | Plain English, short: "Repay", "Confirm", "Transaction completed". "will", not "shall". |
| **Client letter** | replies to complaints, notices, reminders | Polite and formal, «Уважаемый клиент!», «Вы» with a capital В | Polite and plain: "Dear Customer", "you" |
| **Regulatory / report** | CBA regulations, financial statements, AML documents | Terminology of CBA/Russian regulation (IFRS terms in Russian) | IFRS / Basel / FATF English terminology |

The same Armenian word can need different translations in different types: հերթական մարում
is «очередной платеж» in an app but «очередной платеж в погашение кредита» in a contract.

## 2. General rules

- **Translate meaning, not word order.** Armenian puts the verb last and uses long participle
  chains (…ուղղվելու է…). Rebuild the sentence the way Russian or English naturally says it.
- **Do not repeat the same word within a sentence** unless it's a legal defined term.
  Bad: «Данное погашение не считается досрочным погашением». Good: «Данное погашение не является досрочным».
- **One term per concept** across the whole document (see `glossary.tsv`). If the source
  switches words for style, keep one term in translation unless the meaning differs.
- **No omissions and no additions.** Every condition, exception and number stays. Do not add
  explanations inside the text; put them in notes to the user.
- **Keep the modality exactly:** պարտավոր է = obliged (обязан / shall); կարող է = may
  (может / may); իրավունք ունի = entitled (вправе / is entitled to); չի կարող = may not
  (не вправе / may not). Do not turn "may" into "must" or back.
- **Button and screen names** go in quotes as they appear in that language's app:
  Russian «Погасить», English "Repay". If the app's real label is known, use it.
- **Abbreviations:** ՀՀ → РА → RA (or "Republic of Armenia" at first mention in formal text);
  ՀՀ ԿԲ → ЦБ РА → CBA; ԱԱՀ → НДС → VAT; ՀՎՀՀ → ИНН → TIN.

## 3. Russian specifics

- Write **е**, not ё (внесенная, платеж), as Russian banks do in official texts, unless the
  bank's style says otherwise.
- Quotes: «ёлочки»; nested quotes „лапки“.
- Numbers: `1 500 000,50`, `12,5%`, dates `15.03.2026` or `15 марта 2026 г.`
- Currency: `1 500 000 драмов РА` or `1 500 000 AMD`; in tables `AMD`.
- Prefer standard banking phrases:
  - «направить на погашение», not «направить на платеж по погашению»
  - «основной долг» / «основная сумма долга» (for մայր գումար)
  - «остаток задолженности», «очередной платеж», «досрочное погашение», «просроченная задолженность»
  - «излишне уплаченная сумма» / «оставшаяся часть суммы»; «излишек» only in informal text
- Client address in letters and app texts: «Вы», «Ваш» with a capital letter.

## 4. English specifics

- Use one spelling variant per document. Default: **US** spelling ("installment", "canceled"),
  unless the bank's English site uses UK spelling ("instalment", "cancelled").
- Numbers: `1,500,000.50`, `12.5%`; currency code first: `AMD 1,500,000`.
- Dates: `15 March 2026` (never `03/15/2026` or `15/03/2026`).
- Standard terms: principal, outstanding balance, scheduled installment, early repayment
  (or prepayment), overdue amount, penalty, collateral, effective interest rate.
- Contracts: "shall", defined terms with capitals ("the Borrower", "the Loan Agreement").
  Interface texts: short, active voice, no "shall".

## 5. Self-review before delivering

Read the translation on its own, as a native reader would, and then against the source:

1. Would a Russian or English bank publish this wording as is? If a phrase sounds translated, rewrite it.
2. Is every condition, number, date, party and exception from the source still there?
3. Are the obligations as strong as in the source (shall/may/must not)?
4. Are the terms consistent with `glossary.tsv` and within the document?
5. Run `scripts/check.py` and resolve every warning.
