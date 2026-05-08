#!/usr/bin/env python3
import json
import sys
import re

path = sys.argv[1] if len(sys.argv) > 1 else "generated_predictions.jsonl"

total = 0
form_a = 0
form_b = 0
mixed = 0
none = 0
no_think = 0
bad_tool_json = 0

tool_json_re = re.compile(r"<tool_call>\s*(\{.*?\})\s*</tool_call>", re.DOTALL)

def safe_pct(x, n):
    return 0.0 if n == 0 else x / n

with open(path, "r", encoding="utf-8") as f:
    for line_no, line in enumerate(f, 1):
        line = line.strip()
        if not line:
            continue
        total += 1
        try:
            j = json.loads(line)
        except Exception:
            # jsonl 本身坏了
            continue

        pred = j.get("predict", "") or ""
        has_think = "<think>" in pred and "</think>" in pred
        has_ans = "<answer>" in pred and "</answer>" in pred
        has_tool = "<tool_call>" in pred and "</tool_call>" in pred

        if not has_think:
            no_think += 1

        if has_ans and (not has_tool):
            form_a += 1
        elif has_tool and (not has_ans):
            form_b += 1
        elif has_tool and has_ans:
            mixed += 1
        else:
            none += 1

        # 粗检 tool_call 里的 JSON 是否可 parse（只对 Form B / mixed 做）
        if has_tool:
            m = tool_json_re.search(pred)
            if not m:
                bad_tool_json += 1
            else:
                tool_str = m.group(1)
                try:
                    json.loads(tool_str)
                except Exception:
                    bad_tool_json += 1

print("============== Pattern Check (from predict) ==============")
print(f"FILE: {path}")
print(f"TOTAL                : {total}")
print(f"Form A (answer only) : {form_a:6d}  ({safe_pct(form_a,total):.3f})")
print(f"Form B (tool only)   : {form_b:6d}  ({safe_pct(form_b,total):.3f})")
print(f"Mixed (bad)          : {mixed:6d}  ({safe_pct(mixed,total):.3f})")
print(f"Neither A nor B      : {none:6d}  ({safe_pct(none,total):.3f})")
print(f"Missing <think>      : {no_think:6d}  ({safe_pct(no_think,total):.3f})")
print(f"Bad tool JSON (rough): {bad_tool_json:6d}  ({safe_pct(bad_tool_json,total):.3f})")
print("==========================================================")
