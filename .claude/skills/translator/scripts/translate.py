#!/usr/bin/env python3
"""Translate Armenian (hy) text into Russian (ru) and/or English (en) with open-source models.

Engines:
  nllb       facebook/nllb-200-distilled-600M (default, CC-BY-NC-4.0)
  nllb-1.3b  facebook/nllb-200-distilled-1.3B (CC-BY-NC-4.0)
  opus       Helsinki-NLP/opus-mt-hy-{ru,en} (CC-BY-4.0 / Apache-2.0); hy->en pivots through Russian if needed
"""
import argparse
import re
import sys

SRC = "hy"
TARGETS = ("ru", "en")
NAMES = {"hy": "Armenian", "ru": "Russian", "en": "English"}
NLLB_CODES = {"hy": "hye_Armn", "ru": "rus_Cyrl", "en": "eng_Latn"}
NLLB_MODELS = {
    "nllb": "facebook/nllb-200-distilled-600M",
    "nllb-1.3b": "facebook/nllb-200-distilled-1.3B",
}

# Sentence ends: Latin punctuation and the Armenian full stop (U+0589 "։").
# The Armenian question/exclamation marks sit inside the word, so "։" and "." end the sentence.
SENTENCE_END = re.compile(r"(?<=[.!?։…])\s+")


def armenian_share(text):
    """Fraction of letters in the text that are Armenian."""
    letters = [ch for ch in text if ch.isalpha()]
    armenian = [ch for ch in letters if "Ա" <= ch <= "֏" or "ﬓ" <= ch <= "ﬗ"]
    return len(armenian) / len(letters) if letters else 0.0


def split_sentences(paragraph, max_chars=400):
    """Split a paragraph into sentences, then cut any sentence that is still too long."""
    out = []
    for sentence in SENTENCE_END.split(paragraph.strip()):
        while len(sentence) > max_chars:
            cut = sentence.rfind(" ", 0, max_chars)
            cut = cut if cut > 0 else max_chars
            out.append(sentence[:cut])
            sentence = sentence[cut:].lstrip()
        if sentence:
            out.append(sentence)
    return out


class NllbEngine:
    def __init__(self, model_name, device, beams):
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

        self.tokenizer = AutoTokenizer.from_pretrained(model_name, src_lang=NLLB_CODES[SRC])
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)
        self.device = device
        self.beams = beams

    def translate(self, sentences, src, tgt):
        self.tokenizer.src_lang = NLLB_CODES[src]
        batch = self.tokenizer(sentences, return_tensors="pt", padding=True, truncation=True).to(self.device)
        out = self.model.generate(
            **batch,
            forced_bos_token_id=self.tokenizer.convert_tokens_to_ids(NLLB_CODES[tgt]),
            num_beams=self.beams,
            max_new_tokens=512,
        )
        return self.tokenizer.batch_decode(out, skip_special_tokens=True)


class OpusEngine:
    def __init__(self, device, beams):
        self.device = device
        self.beams = beams
        self.cache = {}

    def _load(self, src, tgt):
        key = (src, tgt)
        if key not in self.cache:
            from transformers import MarianMTModel, MarianTokenizer

            name = f"Helsinki-NLP/opus-mt-{src}-{tgt}"
            try:
                tok = MarianTokenizer.from_pretrained(name)
                model = MarianMTModel.from_pretrained(name).to(self.device)
                self.cache[key] = (tok, model)
            except OSError:
                self.cache[key] = None
        return self.cache[key]

    def _direct(self, sentences, pair):
        tok, model = pair
        batch = tok(sentences, return_tensors="pt", padding=True, truncation=True).to(self.device)
        out = model.generate(**batch, num_beams=self.beams, max_new_tokens=512)
        return tok.batch_decode(out, skip_special_tokens=True)

    def translate(self, sentences, src, tgt):
        pair = self._load(src, tgt)
        if pair:
            return self._direct(sentences, pair)
        # No direct hy->en model: pivot through Russian (hy->ru and ru->en both exist).
        first, second = self._load(src, "ru"), self._load("ru", tgt)
        if not (first and second):
            sys.exit(f"No OPUS-MT model for {src}->{tgt}, directly or via Russian. Use --engine nllb.")
        print(f"[opus] no direct {src}->{tgt} model, pivoting through Russian", file=sys.stderr)
        return self._direct(self._direct(sentences, first), second)


def translate_text(engine, text, src, tgt, batch_size=16):
    """Translate paragraph by paragraph so blank-line layout is kept."""
    result = []
    for part in re.split(r"(\n\s*\n)", text):
        if not part.strip():
            result.append(part)
            continue
        sentences = split_sentences(part.replace("\n", " "))
        translated = []
        for i in range(0, len(sentences), batch_size):
            translated.extend(engine.translate(sentences[i : i + batch_size], src, tgt))
        result.append(" ".join(translated))
    return "".join(result)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("text", nargs="*", help="Armenian text to translate (default: --input or stdin)")
    p.add_argument("--to", dest="tgt", default="all", choices=TARGETS + ("all",),
                   help="ru, en, or all for both (default: all)")
    p.add_argument("--engine", default="nllb", choices=("nllb", "nllb-1.3b", "opus"))
    p.add_argument("--input", help="read Armenian text from this file")
    p.add_argument("--output", help="write the translation to this file")
    p.add_argument("--device", default=None, help="cpu or cuda (default: cuda if available)")
    p.add_argument("--beams", type=int, default=4)
    args = p.parse_args()

    if args.text:
        text = " ".join(args.text)
    elif args.input:
        with open(args.input, encoding="utf-8") as f:
            text = f.read()
    else:
        text = sys.stdin.read()
    if not text.strip():
        sys.exit("Nothing to translate.")
    if armenian_share(text) < 0.5:
        sys.exit("The input does not look like Armenian. This skill translates from Armenian only.")

    targets = list(TARGETS) if args.tgt == "all" else [args.tgt]

    import torch

    device = args.device or ("cuda" if torch.cuda.is_available() else "cpu")
    if args.engine == "opus":
        engine = OpusEngine(device, args.beams)
    else:
        engine = NllbEngine(NLLB_MODELS[args.engine], device, args.beams)

    blocks = []
    for tgt in targets:
        out = translate_text(engine, text, SRC, tgt)
        blocks.append(f"[{NAMES[tgt]}]\n{out}" if len(targets) > 1 else out)
    result = "\n\n".join(blocks)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result + "\n")
    else:
        print(result)


if __name__ == "__main__":
    main()
