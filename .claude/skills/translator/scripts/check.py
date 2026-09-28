#!/usr/bin/env python3
"""Check a finished translation against its Armenian source (no models needed).

Reports numbers (amounts, rates, dates, account numbers) missing from the translation and
glossary terms whose expected Russian/English translation is missing.

  python check.py --source src.txt --ru ru.txt --en en.txt
  python check.py --source src.txt --en en.txt

Paragraphs (separated by blank lines) are compared one to one when source and translation
have the same number of paragraphs; otherwise the whole texts are compared.
"""
import argparse
import re
import sys

from translate import NAMES, load_glossary, review_notes


def paragraphs(text):
    return [p for p in re.split(r"\n\s*\n", text) if p.strip()]


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--source", required=True, help="Armenian source text file")
    p.add_argument("--ru", help="Russian translation file")
    p.add_argument("--en", help="English translation file")
    args = p.parse_args()
    if not (args.ru or args.en):
        sys.exit("Pass --ru and/or --en.")

    glossary = load_glossary()
    with open(args.source, encoding="utf-8") as f:
        source = f.read()

    problems = 0
    for tgt, path in (("ru", args.ru), ("en", args.en)):
        if not path:
            continue
        with open(path, encoding="utf-8") as f:
            translation = f.read()
        src_pars, tr_pars = paragraphs(source), paragraphs(translation)
        if len(src_pars) == len(tr_pars):
            pairs = [(f"paragraph {i}", s, t) for i, (s, t) in enumerate(zip(src_pars, tr_pars), 1)]
        else:
            pairs = [("whole text", source, translation)]
        for where, s, t in pairs:
            for note in review_notes(s, t, tgt, glossary):
                print(f"[review] {NAMES[tgt]}, {where}: {note}")
                problems += 1
    if not problems:
        print("[review] no missing numbers or glossary terms found")


if __name__ == "__main__":
    main()
