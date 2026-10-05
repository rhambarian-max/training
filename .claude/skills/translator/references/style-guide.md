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
  - for parts of an amount (ավել մաս, գերավճար, մնացորդ) see section 5
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

## 5. Wording pitfalls

A word for part of an amount must make clear **which part of the money** it means and what it is
measured against. A vague word can point at the wrong money, and in a payment text that changes the meaning.

| Armenian | Meaning | Russian | English | Do not use |
|---|---|---|---|---|
| ավել մասը, ավելցուկը (of a payment) | the part above the required payment | сумма, превышающая размер (очередного) платежа; сумма сверх (очередного) платежа | the amount exceeding the (scheduled) installment; any amount in excess of the installment | «излишек» (colloquial); «оставшаяся часть» / "remaining amount" (reads as the rest or main part of the money) |
| գերավճար | money paid above what is owed | переплата; излишне уплаченная сумма | overpayment | «излишек» |
| մնացորդ (of an account) | what is on the account | остаток (на счете) | balance | bare «остаток» for a loan |
| մնացորդային պարտք | what is still owed on a loan | остаток задолженности | outstanding balance | "remaining debt" in formal text |

When a phrase could point at more than one amount, name the reference amount explicitly
(«сверх очередного платежа», "in excess of the installment"), even if the Armenian leaves it implicit.

Statements of what the client does **not** claim or request (… պահանջ չեմ ներկայացնում) keep the
negation and the legal verb: «не требую» / «не предъявляю требования», "I do not request" /
"I make no claim". Do not turn them into a positive statement ("I agree that…") or a waiver
("I waive…"), which changes the legal meaning.

## 6. Self-review before delivering

Read the translation on its own, as a native reader would, and then against the source:

1. Would a Russian or English bank publish this wording as is? If a phrase sounds translated, rewrite it.
2. Is every condition, number, date, party and exception from the source still there?
3. Does every word for part of an amount (excess, remainder, balance) point at the right money? See section 5.
4. Are the obligations as strong as in the source (shall/may/must not)?
5. Are the terms consistent with `glossary.tsv` and within the document?
6. Run `scripts/check.py` and resolve every warning.
