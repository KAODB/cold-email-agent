#!/usr/bin/env python3
"""Lint a cold-mail draft against the reach-out writing rules.

Draft format:
    To: someone@example.org
    Subject: ...
    <blank line>
    Salutation,
    body...
    --
    signature lines (name, then title)

Usage: check_draft.py DRAFT.md   |   check_draft.py --selftest
Exit 0 = no FAIL, 1 = at least one FAIL, 2 = usage error.
Python standard library only.
"""
import re
import sys

# Plain phrase lists, not NLP. Add a phrase when a bad draft slips through.
OPENERS = [  # banned in the first sentence of the body
    r"\bmy name is\b", r"^i am\b", r"^i'm\b", r"\bhope (you|this)\b", r"\bi wanted to\b",
    r"\bjust wanted\b", r"\bi am writing\b", r"\bi'm writing\b", r"\breaching out\b",
    r"\bintroduce myself\b", r"^我是", r"^我叫", r"冒昧", r"您好.{0,4}我是", r"希望您一切",
]
ANYWHERE = [  # banned anywhere in the body
    # self-intro belongs in the signature, not the body
    r"\bi('m| am) (a|an|the) ", r"\bmy name is\b",
    r"我是.{0,12}(醫師|創辦人|學生|研究生|研究員|工程師|教授|經理|執行長)",
    # needy or filler
    r"pick your brain", r"let me know", r"did you get a chance", r"following up", r"checking in",
    r"circling back", r"look(ing)? forward to hearing", r"any thoughts", r"earliest convenience",
    r"sorry to bother", r"i know you('re| are) busy", r"quick (call|chat|question)", r"hop on a call",
    r"撥冗", r"不知道您(是否|有沒有)", r"再請您", r"期待您的回覆", r"打擾了", r"請多多指教",
]
CJK = re.compile(r"[一-鿿]")
# ASCII-only, so a URL glued to Chinese text ("…/demo。接著") ends at the first non-ASCII char;
# it must end on a URL-ish character, so a sentence-final "?" or "." right after it stays outside.
URL = re.compile(r"https?://[!-~]*[A-Za-z0-9/#=&%~_+-]")
WORD_LIMIT, CHAR_LIMIT, SUBJECT_WORDS = 130, 250, 8  # English words / Chinese chars / subject words


def check(text):
    text = text.replace("\r\n", "\n")
    fails, warns = [], []
    head, _, rest = text.partition("\n\n")
    if not re.search(r"^To:\s*\S+", head, re.M):
        fails.append("no To: line")
    m = re.search(r"^Subject:\s*(.+)$", head, re.M)
    if not m:
        fails.append("no Subject: line")
    elif len(m.group(1).split()) > SUBJECT_WORDS and not CJK.search(m.group(1)):
        warns.append(f"subject longer than {SUBJECT_WORDS} words")
    parts = re.split(r"\n--[ \t]*\n", rest, maxsplit=1)  # editors strip the trailing space of "-- "
    body, sig = parts[0], (parts[1] if len(parts) > 1 else "")
    if len([l for l in sig.splitlines() if l.strip()]) < 2:
        fails.append("signature missing (need '-- ' line, then name and title)")
    lines = [l for l in body.strip().splitlines() if l.strip()]
    if lines and len(lines[0]) < 40 and lines[0].rstrip().endswith((",", "，", ":", "：")):
        lines = lines[1:]  # drop the salutation
    core = "\n".join(lines)
    low = core.lower().replace("’", "'")  # curly apostrophe: "I’m a" counts as "I'm a"
    first = re.split(r"(?<=[.!?。！？])\s*", low.strip(), maxsplit=1)[0]
    for p in OPENERS:
        if re.search(p, first):
            fails.append(f"opening line talks about the sender or is filler: /{p}/")
    for p in ANYWHERE:
        if re.search(p, low):
            fails.append(f"needy or filler phrase: /{p}/")
    no_url = URL.sub("", core)
    if CJK.search(core):
        n, limit = len(re.sub(r"\s", "", no_url)), CHAR_LIMIT
    else:
        n, limit = len(no_url.split()), WORD_LIMIT
    if n > limit:
        fails.append(f"body too long: {n} > {limit}")
    q = len(re.findall(r"[?？]", no_url))  # a '?' inside a URL query string is not a question
    if q != 1:
        fails.append(f"need exactly one question, found {q}")
    if not URL.search(core):
        warns.append("no link in body (is the gift something they can open?)")
    if "—" in core:
        warns.append("em dash in body")
    return fails, warns


BAD = """To: someone@example.org
Subject: Quick question

Dr. X,
Hi, my name is Alex and I hope you are well. Can I pick your brain? Let me know?
"""
GOOD = """To: someone@example.org
Subject: Your field checklist, adapted for new teams

Dr. X,
I'd value one piece of quick expert advice from you, because your field checklist paper is what our pilot is built on. Here is the open version we adapted from it: https://example.org/checklist

If you could cut only one step for teams with no prior training, which step would it be?

We will run the trimmed version next month and send you what came of it.
--
Alex Example
Research engineer
"""
GOOD_ZH = """To: someone@example.org
Subject: 您的現場檢核表，我們拿去試了

王老師，
想請您給一個專家的簡短建議，因為我們的試辦就是照您那篇現場檢核表的論文做的。這是我們改寫後公開的版本：https://example.org/checklist。
如果只能先刪一個步驟給沒受過訓練的團隊用，您會刪哪一步？
我們下個月就照您說的版本試跑，結果整理好寄給您。
--
陳小明
研究工程師
"""


def selftest():
    f, _ = check(BAD)
    assert any("opening line" in x for x in f) and any("needy" in x for x in f), f
    assert any("signature" in x for x in f) and any("exactly one question" in x for x in f), f
    f, w = check(GOOD)
    assert not f and not w, (f, w)
    f, _ = check(GOOD.replace("If you could", "I’m a research engineer on a small team. If you could"))
    assert len(f) == 1 and "needy or filler" in f[0], f  # mid-body self-intro is caught
    f, w = check(GOOD.replace("/checklist", "/checklist?v=2"))
    assert not f and not w, (f, w)  # '?' in a URL query string is not a second question
    f, _ = check(GOOD.replace("it: https://example.org/checklist",
                              "it. Would your teams use https://example.org/checklist?").replace(
        "which step would it be?", "tell me which step it would be."))
    assert not f, f  # a '?' right after a URL still ends the one question
    f, w = check(GOOD_ZH)
    assert not f and not w, (f, w)  # Chinese draft, URL glued to "。"
    bad_zh = GOOD_ZH.replace("想請您給", "冒昧打擾了，我是一名研究所學生。想請您給").replace(
        "寄給您。", "寄給您，期待您的回覆。")
    f, _ = check(bad_zh)
    assert any("opening line" in x for x in f), f
    assert sum("needy" in x for x in f) == 3, f  # self-intro as a student / "looking forward to your reply" / "sorry to bother you"
    f, _ = check(GOOD_ZH.replace("checklist。", "checklist" + "字" * 260))
    assert any("body too long" in x for x in f), f  # Chinese text right after a URL still counts
    print("selftest ok")


def main(argv):
    if argv == ["--selftest"]:
        selftest()
        return 0
    if len(argv) != 1 or argv[0].startswith("-"):
        print("usage: check_draft.py DRAFT.md | check_draft.py --selftest", file=sys.stderr)
        return 2
    with open(argv[0], encoding="utf-8-sig") as fh:
        fails, warns = check(fh.read())
    for x in fails:
        print("FAIL", x)
    for x in warns:
        print("WARN", x)
    print("PASS" if not fails else f"{len(fails)} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
