#!/usr/bin/env python
# Created:2026.06.28

import re
import readline
del readline
from pathlib import Path

def main():
    inp = list(Path().glob("./019_*.org"))[0]
    debug = False
    # debug = True
    print(f"[INFO] 输入文件：{inp}")
    patchf = Path("./patch.conf")
    content = inp.read_text().splitlines()
    if not content:
        print("[INFO] 无有效内容")
        return
    if not debug and patchf.is_file():
        input("[INFO] 将应用补丁文件(回车确定)")
        patch = patchf.read_text().splitlines()
        for l in patch:
            if l.startswith('#') or not l:
                continue
            lineno = int(l[:l.index(':')])
            if lineno >= len(content):
                continue
            text = l[l.index(':')+1:]
            # print(f"SET IDX.{lineno} to {repr(text)}")
            content[lineno] = text
        inp.write_text("\n".join(content))
    else:
        endidx = [idx for idx,l in enumerate(content) if re.match(r"^\* COMMENT ", l)]
        if not endidx:
            print("[INFO] 未找到有效截止点")
            return
        endidx = endidx[-1]
        patchlist = [idx for idx,l in enumerate(content) if 6 < idx < endidx and re.search(r"[A-Za-z]{4,}", l)]
        if debug:
            patchlist = [idx for idx,l in enumerate(content) if 6 < idx < endidx and l]

        origi_text_idx = []
        origi_text = []
        line = ""
        idx = 0
        for idx,l in enumerate(content[endidx+1:]):
            if not line and l:
                line = l
            elif line and l:
                line += " " + l
            if line and not l or l.endswith("\\\\"):
                origi_text_idx.append(idx+endidx+1)
                origi_text.append(line)
                line = ""
        if line:
                origi_text_idx.append(idx+endidx+1)
                origi_text.append(line)

        patchpara = []
        para_idx = 0
        for idx,l in enumerate(content):
            if idx >= endidx:
                break
            if idx in patchlist:
                patchpara.append(para_idx)
            if idx >=6 and l:
                # print(f"[INFO] ==== [{idx}] -- {len(origi_text)} <<<<< {para_idx} ====")
                # print(f"[INFO] {l}")
                # print(f"[INFO] {origi_text[para_idx]}")
                para_idx += 1

        patch = [f"# {origi_text_idx[para]}:{origi_text[para]}\n{idx:d}:{content[idx]}\n" for idx,para in zip(patchlist,patchpara)]
        print("[INFO] 创建补丁文件")
        patchf.write_text("\n".join(patch))

if __name__ == "__main__":
    main()

