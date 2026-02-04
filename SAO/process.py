#!/usr/bin/env python
# Created:2025.09.25

import re
import time
from pathlib import Path

def main():
    s = ""
    for i in Path(".").iterdir():
        if i.suffix != ".txt":
            continue
        ret = ""
        print(f"READ> {i}")
        s = i.read_text(encoding="gbk")
        whiteline = False
        headline = False
        ts = f"{time.strftime("%Y-%m-%d")} {"一二三四五六日"[int(time.strftime("%w"))]} {time.strftime("%H:%M")}"
        s = f"#+title: {i.stem}\n#+date: <{ts}>\n#+setupfile: ../setup.setup\n* Header\n{s}"
        for l in s.splitlines():
            if l.startswith("︵"):
                l = f"#+begin_src text\n{l}"
            elif l.startswith("︶"):
                l = f"{l}\n#+end_src"
            elif l.startswith("===============") and not headline:
                l = f"#+begin_src text\n{l}"
                headline = True
            elif re.match(r"[　]*(第[一二三四五六七八九十]章$|转章.*$)", l):
                match = re.match(r"[　]*(第[一二三四五六七八九十]章$|转章.*$)", l)
                if not match:
                    continue
                l = f"* {match.group(1)}"
                whiteline = True
            elif re.match(r"[　 ]*(\d+)[　 ]*$", l):
                match = re.match(r"[　]*(\d+)[　]*$", l)
                if not match:
                    continue
                l = f"** {match.group(1)}"
                whiteline = True
            elif l.startswith("　　"):
                l = l[2:]
                if not whiteline:
                    l = f"\n{l}"
            if not l:
                if headline:
                    ret += "#+end_src"
                    headline = False
                if whiteline:
                    continue
                whiteline = True
            else:
                whiteline = False
            ret += l+"\n"
        Path(f"{i.stem}.org").write_text(ret, encoding="utf8")

if __name__ == "__main__":
    main()

